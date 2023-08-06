# Callback Support

The tuxsuite cli provides a way to push notification to a given
http(s) based URL at the end of the build/oebuild/test run. The URL
should be passed by the optional argument `--callback` as shown below:

```sh
tuxsuite build \
--git-repo https://github.com/torvalds/linux.git \
--git-ref master \
--target-arch arm \
--toolchain clang-16 \
--kconfig tinyconfig \
--callback https://tuxapi.tuxsuite.com/v1/test_callback
```

__NOTE__: The above callback URL is shown as an example and it does
not exist.

## Security

The JSON data POSTed by Tux backend comes with a security feature
which allows the user to verify that the callback notification comes
from the Tux backend and not anywhere else. There is a signature which
is sent as part of the POST request header called
`x-tux-payload-signature`. This signature is base64 encoded and can be
used to verify the authenticity of the sender of the notification.

Following is the verification code in Python:

```py
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)


def verify(public_key: str, signature: str, payload: str):
   """Function to illustrate the verification of the signature."""
   signature = base64.urlsafe_b64decode(signature)
   key = serialization.load_ssh_public_key(public_key.encode("ascii"))
       try:
           key.verify(
               signature,
               payload.encode("utf-8"),
               ec.ECDSA(hashes.SHA256()),
           )
           return True
       except InvalidSignature:
           return False
```

- **public_key**: The public key should be cached in the user's server
  that accepts the push notification. The public key for a specific Tux
  group (`tuxsuite` in this case) can be obtained as follows:

```sh
curl https://tuxapi.tuxsuite.com/v1/groups/tuxsuite/keys -O public_key.txt
```

- **signature**: This is the signature that is sent with the
  `x-tux-payload-signature` header in the request.

- **payload**: The JSON payload is sent as part of the request. The
  value of `kind` in the JSON, will be one of
  build/oebuild/test. Following is a sample JSON  payload, for
  illustration:

<details>
<summary>Click to see payload sample</summary>

```json
{
    "kind": "test",
    "status": {
        "ap_romfw": null,
        "bios": null,
        "bl1": null,
        "boot_args": null,
        "callback": "https://tuxapi.tuxsuite.com/v1/test_callback",
        "device": "qemu-arm64",
        "download_url": "https://storage.tuxsuite.com/public/tuxsuite/demo/tests/2MBYa8FhoBHkRCX2BMMPusjuClf/",
        "dtb": null,
        "duration": 117,
        "finished_time": "2023-02-24T12:44:23.178581",
        "fip": null,
        "is_canceling": false,
        "is_public": true,
        "kernel": "https://storage.tuxsuite.com/public/linaro/lkft/builds/2M0PXsQDVWO3DwIKTIlwtDELTpb/Image.gz",
        "mcp_fw": null,
        "mcp_romfw": null,
        "modules": "https://storage.tuxsuite.com/public/linaro/lkft/builds/2M0PXsQDVWO3DwIKTIlwtDELTpb/modules.tar.xz",
        "parameters": {
            "SHARD_INDEX": "4",
            "SHARD_NUMBER": "10",
            "SKIPFILE": "skipfile-lkft.yaml"
        },
        "plan": null,
        "project": "tuxsuite/demo",
        "provisioning_time": "2023-02-24T12:41:42.541788",
        "result": "pass",
        "results": {
            "boot": "pass"
        },
        "retries": 0,
        "retries_messages": [],
        "rootfs": "https://storage.tuxsuite.com/public/linaro/lkft/oebuilds/2LjyTGHSPqxUqtyCl1xI7SCrbWp/images/juno/lkft-tux-image-juno-20230214185536.rootfs.ext4.gz",
        "running_time": "2023-02-24T12:42:27.314447",
        "scp_fw": null,
        "scp_romfw": null,
        "state": "finished",
        "tests": [
            "boot"
        ],
        "timeouts": {},
        "token_name": "demo-tuxsuite",
        "uefi": null,
        "uid": "2MBYa8FhoBHkRCX2BMMPusjuClf",
        "user": "demo.user@linaro.org",
        "user_agent": "tuxsuite/1.9.0",
        "waiting_for": null
    }
}
```

</details>

__NOTE__: The Tux backends use ECDSA based cryptogrphic key pairs in order to
create the signature.
