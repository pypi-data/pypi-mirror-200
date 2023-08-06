# -*- coding: utf-8 -*-

import sys
import json

from tuxsuite.cli.requests import (
    delete,
    get,
    post,
    put,
)
from tuxsuite.cli.utils import error


def check_required_cmdargs(cmdargs):
    if not cmdargs.token:
        sys.stderr.write("--token is required\n")
        sys.exit(1)
    if not cmdargs.username:
        sys.stderr.write("--username is required\n")
        sys.exit(1)
    if not cmdargs.domain:
        sys.stderr.write("--domain is required\n")
        sys.exit(1)


def handle_add(cmdargs, _, config):
    data = {}
    kind = cmdargs.kind[0]
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys"
    if kind not in ["pat"]:  # The list may get expanded in future
        error(f"Unknown key kind. Is '{kind}' a valid key supported by TuxSuite?\n")

    if kind == "pat":
        check_required_cmdargs(cmdargs)
        data["kind"] = kind
        data["key"] = {
            "pat": cmdargs.token,
            "username": cmdargs.username,
            "domain": cmdargs.domain,
        }

    ret = post(config, url, data=data)

    if ret.status_code != 201:
        error(f"Failed to add '{kind}' key '{cmdargs.domain}:{cmdargs.username}'")
    else:
        print(f"'{kind}' key '{cmdargs.domain}:{cmdargs.username}' added")
        sys.exit(0)


def handle_get(cmdargs, _, config):
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys"
    ret = get(config, url)

    if ret.status_code != 200:
        error("Failed to get the keys")
    else:
        keys = ret.json()
        if cmdargs.json:
            print(json.dumps(ret.json(), indent=True))
        else:
            print(f"ssh public key:\n\n{keys['ssh']['pub']}\n")
            pat_keys = keys.get("pat")
            if pat_keys:  # Required to print the 'pat keys:' heading
                print("pat keys:\n")
                print("s.no\tdomain\t\t\tusername\t\ttoken\n")
                for count, pat in enumerate(pat_keys, start=1):
                    print(
                        f"{count}.\t{pat['domain']}\t\t{pat['username']}\t\t{pat['pat']}"
                    )
        sys.exit(0)


def handle_delete(cmdargs, _, config):
    kind = cmdargs.kind[0]
    if kind not in ["pat"]:  # The list may get expanded in future
        error(f"Unknown key kind. Is '{kind}' a valid key supported by TuxSuite?\n")

    if kind == "pat":
        if not cmdargs.domain:
            sys.stderr.write("--domain is required\n")
            sys.exit(1)
        if not cmdargs.username:
            sys.stderr.write("--username is required\n")
            sys.exit(1)
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys/{kind}/{cmdargs.domain}/{cmdargs.username}"
    ret = delete(config, url)

    if ret.status_code != 200:
        error(f"Failed to delete '{kind}' key '{cmdargs.domain}:{cmdargs.username}'")
    else:
        print(f"'{kind}' key '{cmdargs.domain}:{cmdargs.username}' deleted")
        sys.exit(0)


def handle_update(cmdargs, _, config):
    data = {}
    kind = cmdargs.kind[0]
    url = f"/v1/groups/{config.group}/projects/{config.project}/keys"
    if kind not in ["pat"]:  # The list may get expanded in future
        error(f"Unknown key kind. Is '{kind}' a valid key supported by TuxSuite?\n")

    if kind == "pat":
        check_required_cmdargs(cmdargs)
        data["kind"] = kind
        data["key"] = {
            "pat": cmdargs.token,
            "username": cmdargs.username,
            "domain": cmdargs.domain,
        }

    ret = put(config, url, data=data)

    if ret.status_code != 201:
        error(f"Failed to update '{kind}' key '{cmdargs.domain}:{cmdargs.username}'")
    else:
        print(f"'{kind}' key '{cmdargs.domain}:{cmdargs.username}' updated")
        sys.exit(0)


handlers = {
    "add": handle_add,
    "get": handle_get,
    "delete": handle_delete,
    "update": handle_update,
}


def keys_cmd_common_options(sp):
    sp.add_argument(
        "--domain",
        help="Domain for the given key",
        default=None,
        type=str,
    )
    sp.add_argument(
        "kind",
        metavar="kind",
        help="Kind of the key {pat}",
        nargs=1,
    )


def keys_cmd_token_option(sp):
    sp.add_argument(
        "--token",
        help="Value of the Personal Access Token (PAT)",
        default=None,
        type=str,
    )


def keys_cmd_username_option(sp):
    sp.add_argument(
        "--username",
        help="Username for the given key",
        default=None,
        type=str,
    )


def setup_parser(parser):
    # "keys add"
    t = parser.add_parser("add")
    keys_cmd_common_options(t)
    keys_cmd_token_option(t)
    keys_cmd_username_option(t)

    # "keys get"
    t = parser.add_parser("get")
    t.add_argument(
        "--json",
        help="output json to stdout",
        default=False,
        action="store_true",
    )

    # "keys delete"
    t = parser.add_parser("delete")
    keys_cmd_common_options(t)
    keys_cmd_username_option(t)

    # "keys update"
    t = parser.add_parser("update")
    keys_cmd_common_options(t)
    keys_cmd_token_option(t)
    keys_cmd_username_option(t)

    return sorted(parser._name_parser_map.keys())
