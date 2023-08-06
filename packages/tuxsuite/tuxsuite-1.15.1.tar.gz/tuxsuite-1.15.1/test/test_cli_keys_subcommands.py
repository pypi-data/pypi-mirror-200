# -*- coding: utf-8 -*-

import sys
import json
import pytest
import tuxsuite


@pytest.fixture
def keys_json():
    keys = {
        "ssh": {"pub": "ecdsa-sha2-nistp256 AAAADianw="},
        "pat": [
            {"pat": "****", "username": "test-user-2", "domain": "gitlab.com"},
            {"pat": "****", "username": "test-user-4", "domain": "github.com"},
        ],
    }
    return json.dumps(keys, indent=True).encode("utf-8")


def test_keys_handle_get(mocker, keys_json, config, response, monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "get"])
    response.status_code = 200
    response._content = keys_json
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "ssh public key:" in output
    assert exc_info.value.code == 0
    assert get_req.call_count == 1

    # # Test json out
    monkeypatch.setattr(
        sys,
        "argv",
        ["tuxsuite", "keys", "get", "--json"],
    )
    response.status_code = 200
    response._content = keys_json
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    assert exc_info.value.code == 0
    assert get_req.call_count == 1

    # Test failure case when the response is not 200
    response.status_code = 400
    response._content = {}
    get_req = mocker.patch("requests.get", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    assert get_req.call_count == 1
    assert exc_info.value.code == 1
    output, error = capsys.readouterr()
    assert "Error: Failed to get the keys\n" == error


def test_keys_handle_add(mocker, keys_json, config, response, monkeypatch, capsys):
    # wrong key kind
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "add", "unknown-kind"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert (
        "Unknown key kind. Is 'unknown-kind' a valid key supported by TuxSuite?\n"
        in error
    )
    assert exc_info.value.code == 1

    # without required options
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "add", "pat"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--token is required" in error
    assert exc_info.value.code == 1

    # without username and domain options
    mocker.resetall()
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "keys", "add", "pat", "--token", "test-token"]
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--username is required" in error
    assert exc_info.value.code == 1

    # without domain option
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
        ],
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required" in error
    assert exc_info.value.code == 1

    # happy flow
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 201
    response._content = {}
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'pat' key 'gitlab.com:test-user-1' added\n" == output
    assert post_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "add",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 400
    response._content = {}
    post_req = mocker.patch("requests.post", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to add 'pat' key 'gitlab.com:test-user-1'\n" == error
    assert post_req.call_count == 1
    assert exc_info.value.code == 1


def test_keys_handle_delete(mocker, keys_json, config, response, monkeypatch, capsys):
    # wrong key kind
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "delete", "unknown-kind"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert (
        "Unknown key kind. Is 'unknown-kind' a valid key supported by TuxSuite?\n"
        in error
    )
    assert exc_info.value.code == 1

    # without required options
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "delete", "pat"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required" in error
    assert exc_info.value.code == 1

    # without required options
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "keys", "delete", "pat", "--domain", "gitlab.com"]
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--username is required" in error
    assert exc_info.value.code == 1

    # happy flow
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "delete",
            "pat",
            "--domain",
            "gitlab.com",
            "--username",
            "test-user-1",
        ],
    )
    response.status_code = 200
    response._content = {}
    delete_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'pat' key 'gitlab.com:test-user-1' deleted\n" == output
    assert delete_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "delete",
            "pat",
            "--domain",
            "unknown",
            "--username",
            "test-user-1",
        ],
    )
    response.status_code = 400
    response._content = {}
    delete_req = mocker.patch("requests.delete", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to delete 'pat' key 'unknown:test-user-1'\n" == error
    assert delete_req.call_count == 1
    assert exc_info.value.code == 1


def test_keys_handle_update(mocker, keys_json, config, response, monkeypatch, capsys):
    # wrong key kind
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "update", "unknown-kind"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert (
        "Unknown key kind. Is 'unknown-kind' a valid key supported by TuxSuite?\n"
        in error
    )
    assert exc_info.value.code == 1

    # without required options
    monkeypatch.setattr(sys, "argv", ["tuxsuite", "keys", "update", "pat"])
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--token is required" in error
    assert exc_info.value.code == 1

    # without username and domain options
    mocker.resetall()
    monkeypatch.setattr(
        sys, "argv", ["tuxsuite", "keys", "update", "pat", "--token", "test-token"]
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--username is required" in error
    assert exc_info.value.code == 1

    # without domain option
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
        ],
    )
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "--domain is required" in error
    assert exc_info.value.code == 1

    # happy flow
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 201
    response._content = {}
    put_req = mocker.patch("requests.put", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "'pat' key 'gitlab.com:test-user-1' updated\n" == output
    assert put_req.call_count == 1
    assert exc_info.value.code == 0

    # failed request
    mocker.resetall()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "tuxsuite",
            "keys",
            "update",
            "pat",
            "--token",
            "test-token",
            "--username",
            "test-user-1",
            "--domain",
            "gitlab.com",
        ],
    )
    response.status_code = 400
    response._content = {}
    put_req = mocker.patch("requests.put", return_value=response)
    with pytest.raises(SystemExit) as exc_info:
        tuxsuite.cli.main()
    output, error = capsys.readouterr()
    assert "Error: Failed to update 'pat' key 'gitlab.com:test-user-1'\n" == error
    assert put_req.call_count == 1
    assert exc_info.value.code == 1
