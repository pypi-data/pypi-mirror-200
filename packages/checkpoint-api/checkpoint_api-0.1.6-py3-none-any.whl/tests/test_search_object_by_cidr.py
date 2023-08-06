import json

import responses

from checkpoint_api.checkpoint import CheckpointSession
from checkpoint_api.enumerations import ObjectType

login_json_ok = {
    "sid": "sl8x_2ZNhJGpLW21GIYSLVFKu6iHi79adLXKOBYsDc8",
    "url": "https://10.100.30.25:443/web_api",
    "session-timeout": 600,
    "last-login-was-at": {"posix": 1601036144322, "iso-8601": "2020-09-25T14:15+0200"},
    "read-only": True,
    "api-server-version": "1.6.1",
}

search_json_ok = {
    "from": 1,
    "to": 1,
    "total": 1,
    "objects": [
        {
            "uid": "8874eceb-e217-476e-a16c-b1ec2926b921",
            "name": "IP_10.14.33.6_xlnetp02",
            "type": "host",
            "domain": {
                "uid": "41e821a0-3720-11e3-aa6e-0800200c9fde",
                "name": "SMC User",
                "domain-type": "domain",
            },
            "ipv4-address": "10.14.33.6",
        }
    ],
}
search_json_empty = []


@responses.activate
def test_search_01():
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
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/show-objects",
        json=search_json_empty,
        status=200,
    )

    with CheckpointSession("10.100.30.25", "api", "topsecret", logfile="") as cps:
        response_json = cps.search_object_by_cidr("10.14.33.33", type=ObjectType.HOST)
        assert response_json == search_json_empty

    assert len(responses.calls) == 3


@responses.activate
def test_search_02():
    def request_callback(request):
        data = json.loads(request.body)
        resp_body = search_json_ok["objects"]
        return 200, {}, json.dumps(resp_body)

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
    responses.add_callback(
        responses.POST,
        "https://10.100.30.25/web_api/show-objects",
        callback=request_callback,
    )

    with CheckpointSession(
        "10.100.30.25", "api", "topsecret", logfile="checkpoint.log"
    ) as cps:
        response_json = cps.search_object_by_cidr("10.14.33.6", type=ObjectType.HOST)
        assert response_json == search_json_ok["objects"]

    assert len(responses.calls) == 3


@responses.activate
def test_search_03():
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
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/show-objects",
        json=search_json_empty,
        status=200,
    )

    with CheckpointSession("10.100.30.25", "api", "topsecret", logfile="") as cps:
        response_json = cps.search_object_by_cidr("99.99.99.99")
        assert response_json == search_json_empty
        response_json = cps.search_object_by_cidr("99.99.99.99", type=ObjectType.HOST)
        assert response_json == search_json_empty

    assert len(responses.calls) == 4
