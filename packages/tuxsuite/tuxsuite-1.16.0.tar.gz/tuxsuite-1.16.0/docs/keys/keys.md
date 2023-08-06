# Keys

The `keys` sub-command provides a way to manage per project credentials
/ keys in TuxSuite. These keys will be used in order to access private
repositories during a build/oebuild whenever requested. The keys
feature is not available for community users. This sub-command
supports the following key types:

* Personal Access Token (pat)
* Secure Shell (ssh)

**__NOTE:__** This command only allows viewing the public key of the stored
ssh key for the given group. The ssh key is generated per group by the
TuxSuite team.

## add

The `add` sub-sub-command is used to add a new key to a specific
project. The current support provides adding personal access tokens
(pat) or http username/passwords for any git server domain with
supported protocols, for example github or gitlab.

```shell
tuxsuite keys add pat --domain gitlab.com --username test-user-1 --token your-secret-token
```

In the above command, a new key of kind `pat` is being added whose
domain is provided with the `--domain` option, username is provided with
`--username` option and token is provided with the `--token`
option. The group and project is not explicitly mentioned in this
command, which is obtained from the config file
`~/.config/tuxsuite/config.ini` or the `GROUP` and `PROJECT`
environment variables.

The following options are mandatory for the `add` sub-sub-command:

* --domain
* --username
* --token

## delete

The `delete` sub-sub-command is used to delete an already added key
from a project with a specific domain and username.

```shell
tuxsuite keys delete pat --domain gitlab.com --username test-user-1
```

In the above command, an existing key of kind `pat` for the domain
`gitlab.com` with username `test-user-1` is deleted for the project
which is obtained from the config file `~/.config/tuxsuite/config.ini`
or the `GROUP` and `PROJECT` environment variables.

The following options are mandatory for the `delete` sub-sub-command:

* --domain
* --username

## get

The `get` sub-sub-command is used to list all the available keys for a
project.

```shell
tuxsuite keys get
```

<details>
<summary>Click to see output</summary>

```
ssh public key:

ecdsa-sha2-nistp256 AAAAE2Vjanw=

pat keys:

s.no    domain        username        token

1.      github.com    test-user-1     ****
2.      gitlab.com    test-user-1     ****
3.      gitlab.com    test-user-2     ****
4.      github.com    test-user-2     ****
```

</details>

Use `--json` option to get the list of keys in JSON format printed to
stdout.

```shell
tuxsuite keys get --json
```

<details>
<summary>Click to see JSON output</summary>

```json
{
 "ssh": {
  "pub": "ecdsa-sha2-nistp256 AAAAE2Vjanw="
 },
 "pat": [
  {
   "pat": "****",
   "username": "test-user-1",
   "domain": "gitlab.com"
  },
  {
   "pat": "****",
   "username": "test-user-3",
   "domain": "gitlab.com"
  },
  {
   "pat": "****",
   "username": "test-user-1",
   "domain": "github.com"
  },
  {
   "pat": "****",
   "username": "test-user-2",
   "domain": "github.com"
  },
  {
   "pat": "****",
   "username": "test-user-4",
   "domain": "gitlab.com"
  }
 ]
}
```

</details>

## update

The `update` sub-sub-command is used to update an existing key already
added to a specific project.

```shell
tuxsuite keys update pat --domain gitlab.com --username test-user-1 --token your-new-secret-token
```

In the above command, the existing key of kind `pat` is being updated
with a new token whose domain is provided with the `--domain` option,
username is provided with `--username` option and the new token is
provided with the `--token` option. The group and project is not
explicitly mentioned in this command, which is obtained from the
config file `~/.config/tuxsuite/config.ini` or the `GROUP` and
`PROJECT` environment variables.

The following options are mandatory for the `update` sub-sub-command:

* --domain
* --username
* --token
