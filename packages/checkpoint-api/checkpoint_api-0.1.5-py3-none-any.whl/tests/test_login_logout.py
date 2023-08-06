import json

import pytest
import requests
import responses

from checkpoint_api.checkpoint import CheckpointSession
from checkpoint_api.exceptions import (
    CheckpointMissingCredentialsException,
    CheckpointTooManyCredentialsException,
)

login_json_ok = {
    "sid": "sl8x_2ZNhJGpLW21GIYSLVFKu6iHi79adLXKOBYsDc8",
    "url": "https://10.100.30.25:443/web_api",
    "session-timeout": 600,
    "last-login-was-at": {"posix": 1601036144322, "iso-8601": "2020-09-25T14:15+0200"},
    "read-only": True,
    "api-server-version": "1.6.1",
}

login_json_failed = {
    "code": "err_login_failed",
    "message": "Authentication to server failed.",
}


def test_login_credentials():
    with pytest.raises(CheckpointMissingCredentialsException):
        with CheckpointSession("10.100.30.25", logfile="") as cps:
            pass
    with pytest.raises(CheckpointMissingCredentialsException):
        with CheckpointSession("10.100.30.25", "test_user", logfile="") as cps:
            pass
    with pytest.raises(CheckpointTooManyCredentialsException):
        with CheckpointSession(
            "10.100.30.25", "user", "topsecretpass", api_key="asdasdasfasf", logfile=""
        ) as cps:
            pass


@responses.activate
def test_login_handling_01():
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/login",
        json=login_json_ok,
        status=200,
    )
    responses.add(
        responses.POST, "https://10.100.30.25/web_api/logout", json={}, status=200
    )
    responses.add(
        responses.POST, "https://10.100.30.25/web_api/discard", json={}, status=200
    )

    with CheckpointSession(
        "10.100.30.25", "api", "topsecret", logfile="checkpoint.log"
    ) as cps:
        assert cps.sid == login_json_ok["sid"]

    with CheckpointSession(
        "10.100.30.25", api_key="topsecretapikey", logfile="checkpoint.log"
    ) as cps:
        assert cps.sid == login_json_ok["sid"]

    assert len(responses.calls) == 4


@responses.activate
def test_login_handling_02():
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/login",
        json=login_json_failed,
        status=400,
    )
    with pytest.raises(Exception):
        with CheckpointSession("10.100.30.25", "api", "topsecret", logfile="") as cps:
            pass
    assert len(responses.calls) == 1


@responses.activate
def test_login_handling_03():
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/login",
        json=login_json_ok,
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/logout",
        json={"code": "error", "message": "Error logging out"},
        status=500,
    )
    responses.add(
        responses.POST, "https://10.100.30.25/web_api/discard", json={}, status=200
    )
    with pytest.raises(Exception):
        with CheckpointSession(
            "10.100.30.25", "api", "topsecret", domain="CPP", logfile=""
        ) as cps:
            assert cps.sid == login_json_ok["sid"]

        assert len(responses.calls) == 2


@responses.activate
def test_unmatched_endpoint_raises_connection_error():
    responses.add(
        responses.POST,
        "https://10.100.30.251/web_api/login",
        body=requests.exceptions.ConnectionError(
            "HTTPSConnectionPool(host='10.100.30.251', port=443): Max retries exceeded with url: /web_api/login (Caused by NewConnectionError('<urllib3.connection.HTTPSConnection object at 0x0000023115769F40>: Failed to establish a new connection: [WinError 10061] No connection could be made because the target machine actively refused it')"
        ),
    )
    with pytest.raises(requests.exceptions.ConnectionError):
        with CheckpointSession("10.100.30.251", "api", "topsecret", logfile="") as cps:
            pass


@responses.activate
def test_unmatched_endpoint_raises_generic_error():
    responses.add(
        responses.POST,
        "https://10.100.30.251/web_api/login",
        body=requests.exceptions.ConnectionError(
            "Exception: 400: generic_error - Runtime error: Domain 'CPP2' not found!"
        ),
    )
    with pytest.raises(Exception):
        with CheckpointSession(
            "10.100.30.25", "api", "topsecret", domain="CPP2", logfile=""
        ) as cps:
            pass


@responses.activate
def test_using_a_callback_for_dynamic_responses():
    def request_callback(request):
        return 666, {}, json.dumps({})

    responses.add_callback(
        responses.POST,
        "https://10.122.0.112/web_api/login",
        callback=request_callback,
        content_type="application/json",
    )
    responses.add(
        responses.POST, "https://10.122.0.112/web_api/logout", json={}, status=200
    )
    responses.add(
        responses.POST, "https://10.100.30.25/web_api/discard", json={}, status=200
    )
    with pytest.raises(Exception) as excinfo:
        with CheckpointSession(
            "10.122.0.112", "api", "topsecret", domain="CPP2", logfile=""
        ) as cps:
            pass
    assert str(excinfo.value) == "666: err - 'code'"
