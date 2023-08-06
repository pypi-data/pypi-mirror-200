# -*- coding: utf-8 -*-

import pytest
from itertools import chain
from tuxsuite.cli.utils import (
    datediff,
    file_or_url,
    key_value,
    show_log,
    format_plan_result,
)
from tuxsuite import Plan


def test_datediff():
    assert datediff("hello", "hello") == "\x1b[37mhello\x1b[0m"
    assert datediff("hello world", "hello monde") == "\x1b[37mhello \x1b[0mmonde"


def test_key_value(mocker):
    error = mocker.patch("tuxsuite.cli.utils.error", side_effect=Exception)
    assert key_value("HELLO=WORLD") == ("HELLO", "WORLD")
    with pytest.raises(Exception):
        key_value("HELLO=WORLD=1")
    error.assert_called_once_with("Key Value pair not valid: HELLO=WORLD=1")

    error.reset_mock()
    with pytest.raises(Exception):
        key_value("HELLO world")
    error.assert_called_once_with("Key Value pair not valid: HELLO world")


def test_file_or_url():
    url = "http://www.example.com/"
    result = file_or_url(url)
    assert result == url

    with pytest.raises(SystemExit):
        file_or_url("/temp/unknown")


def test_show_log(mocker, build):
    mocker.patch("tuxsuite.build.Build.get_status", return_value={"download_url": ""})
    mocker.patch("tuxsuite.build.Build.warnings_count", return_value=1)
    with pytest.raises(SystemExit):
        show_log(build, False, None)


def test_format_plan_result(config, capsys):
    plan_obj = Plan("")

    def get_plan():
        return {
            "builds": {
                "2KgXpq96Y4bh06h3Zd4vvgUZfiP": {
                    "project": "tuxsuite/alok",
                    "uid": "2KgXpq96Y4bh06h3Zd4vvgUZfiP",
                    "plan": "2KgXpWIVjTZew6qAzDH47PuzkTG",
                    "build_name": "kernel builds",
                    "git_repo": "git://test_repo",
                    "git_ref": "master",
                    "kconfig": "test-config",
                    "target_arch": "x86_64",
                    "toolchain": "gcc-8",
                    "state": "finished",
                    "result": "canceled",
                    "build_status": "canceled",
                    "tuxbuild_status": "canceled",
                    "status_message": "Build canceled on request",
                },
                "2KgXplER4lGN5hvUhT5HMuH3lbq": {
                    "project": "tuxsuite/alok",
                    "uid": "2KgXplER4lGN5hvUhT5HMuH3lbq",
                    "plan": "2KgXpWIVjTZew6qAzDH47PuzkTG",
                    "build_name": "",
                    "git_repo": "git://test_repo",
                    "git_ref": "master",
                    "kconfig": "test-config",
                    "target_arch": "x86_64",
                    "toolchain": "gcc-9",
                    "state": "finished",
                    "result": "unknown",
                    "build_status": "unknown",
                    "tuxbuild_status": "unknown",
                },
            },
            "tests": {},
        }

    plan_obj.load(get_plan())
    for b in chain(plan_obj.canceled(), plan_obj.unknown()):
        format_plan_result(b, plan_obj._tests_wait_for(b.uid))
    out, err = capsys.readouterr()
    assert err == ""
    assert (
        out
        == "2KgXpq96Y4bh06h3Zd4vvgUZfiP ⚠️  Canceled with toolchain: gcc-8 target_arch: x86_64\n\
2KgXplER4lGN5hvUhT5HMuH3lbq 🧐 Unknown with toolchain: gcc-9 target_arch: x86_64\n"
    )
