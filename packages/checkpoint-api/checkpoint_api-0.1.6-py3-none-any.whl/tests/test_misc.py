import json

import responses
import pytest

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

add_host_json_ok = {
    "uid": "9423d36f-2d66-4754-b9e2-e7f4493756d4",
    "folder": {
        "uid": "feb54da1-c5e2-4e83-a3ed-d0601ba5ccb9",
        "name": "/Global Objects",
    },
    "domain": {
        "domain-type": "local domain",
        "uid": "41e821a0-3720-11e3-aa6e-0800200c9fde",
        "name": "SMC User",
    },
    "meta-info": {
        "lock": "unlocked",
        "validation-state": "ok",
        "read-only": False,
        "last-modify-time": {
            "posix": 1429440561055,
            "iso-8601": "2015-04-19T13:49+0300",
        },
        "last-modifier": "aa",
        "creation-time": {"posix": 1429440561055, "iso-8601": "2015-04-19T13:49+0300"},
        "creator": "aa",
    },
    "tags": [],
    "name": "host1",
    "comments": "",
    "color": "black",
    "icon": "Objects/host",
    "groups": [],
    "nat-settings": {"auto-rule": False},
    "ipv4-address": "192.0.1.1",
    "ipv6-address": "",
}

show_hosts_json_ok = {
    "from": 1,
    "to": 2,
    "total": 10,
    "objects": [
        {
            "uid": "6b6bf76d-9f9e-4655-bd2f-ca2db753fb94",
            "name": "host_1",
            "type": "host",
            "domain": {
                "uid": "a59b701f-79dd-49dd-b054-f3c92af4b608",
                "name": "dom82",
                "domain-type": "domain",
            },
            "icon": "Objects/host",
            "color": "cyan",
            "ipv4-address": "88.5.9.77",
        },
        {
            "uid": "94a3f624-48f2-4630-97cd-4468c7ca5af8",
            "name": "host_2",
            "type": "host",
            "domain": {
                "uid": "a59b701f-79dd-49dd-b054-f3c92af4b608",
                "name": "dom82",
                "domain-type": "domain",
            },
            "icon": "Objects/host",
            "color": "black",
            "ipv4-address": "43.77.34.4",
        },
    ],
}


@responses.activate
def test_encoding_01():
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
        "https://10.100.30.25/web_api/show-version",
        json={"value": "öäü"},
        status=200,
    )

    with CheckpointSession("10.100.30.25", "api", "topsecret", logfile="") as cps:
        response_json = cps.post("show-version", json={})
        assert response_json == {"value": "öäü"}

    assert len(responses.calls) == 3


@responses.activate
def test_discard_01():
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
        "https://10.100.30.25/web_api/publish",
        json={"task-id": 4711},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/show-task",
        json={"tasks": [{"status": "succeeded"}]},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/add-host",
        json=add_host_json_ok,
        status=200,
    )

    with CheckpointSession(
        "10.100.30.25", "api", "topsecret", logfile="checkpoint.log", read_only=False
    ) as cps:
        response_json = cps.post(
            "add-host", json={"name": "host1", "ip-address": "192.0.1.1"}
        )
        cps.discard()

    assert len(responses.calls) == 5


@responses.activate
def test_paginate_01():
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
        "https://10.100.30.25/web_api/show-hosts",
        json={
            "objects": [{"name": "host1"}, {"name": "host2"}],
            "to": 2,
            "from": 0,
            "total": 10,
        },
        status=200,
    )

    with CheckpointSession("10.100.30.25", api_key="apisecretkey") as cps:
        json_rulebase_export = cps.post_paginate("show-hosts", json={"limit": 2})

    with CheckpointSession("10.100.30.25", api_key="apisecretkey") as cps:
        json_rulebase_export = cps.post_paginate("show-hosts", json={})


@responses.activate
def test_paginate_02():
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
        "https://10.100.30.25/web_api/show-hosts",
        json={
            "objects": [{"name": "host1"}, {"name": "host2"}],
        },
        status=200,
    )

    with CheckpointSession("10.100.30.25", api_key="apisecretkey") as cps:
        json_rulebase_export = cps.post_paginate("show-hosts", json={"limit": 2})


@responses.activate
def test_get_groups():
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
        responses.POST, "https://10.100.30.25/web_api/show-groups", json={}, status=200
    )

    with CheckpointSession("10.100.30.25", api_key="apisecretkey") as cps:
        groups = cps.get_groups()


@responses.activate
def test_publish_01():
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
        "https://10.100.30.25/web_api/publish",
        json={"task-id": 4711},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/show-task",
        json={"tasks": [{"status": "succeeded"}]},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/add-host",
        json=add_host_json_ok,
        status=200,
    )

    with CheckpointSession(
        "10.100.30.25", "api", "topsecret", logfile="checkpoint.log", read_only=False
    ) as cps:
        response_json = cps.post(
            "add-host", json={"name": "host1", "ip-address": "192.0.1.1"}
        )
        cps.publish()

    assert len(responses.calls) == 6


@responses.activate
def test_publish_02():
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
        "https://10.100.30.25/web_api/publish",
        json={"task-id": 4711},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/show-task",
        json={"tasks": [{"status": "in progress"}]},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/add-host",
        json=add_host_json_ok,
        status=200,
    )

    with pytest.raises(Exception):
        with CheckpointSession(
            "10.100.30.25",
            "api",
            "topsecret",
            logfile="checkpoint.log",
            read_only=False,
        ) as cps:
            response_json = cps.post(
                "add-host", json={"name": "host1", "ip-address": "192.0.1.1"}
            )
            cps.publish(sleep=0)

    assert len(responses.calls) == 105


@responses.activate
def test_policy_install_01():
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
        "https://10.100.30.25/web_api/install-policy",
        json={"task-id": "123456"},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/show-task",
        json={"tasks": [{"status": "succeeded"}]},
        status=200,
    )

    with CheckpointSession(
        "10.100.30.25", "api", "topsecret", logfile="checkpoint.log", read_only=False
    ) as cps:
        response_json = cps.policy_install("standard", ["fw1"])

    assert len(responses.calls) == 5


@responses.activate
def test_policy_install_02():
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
        "https://10.100.30.25/web_api/install-policy",
        json={"task-id": "123456"},
        status=200,
    )
    responses.add(
        responses.POST,
        "https://10.100.30.25/web_api/show-task",
        json={"tasks": [{"status": "unknown"}]},
        status=200,
    )

    with pytest.raises(Exception):
        with CheckpointSession(
            "10.100.30.25",
            "api",
            "topsecret",
            logfile="checkpoint.log",
            read_only=False,
        ) as cps:
            response_json = cps.policy_install("standard", ["fw1"])

        assert len(responses.calls) == 5
