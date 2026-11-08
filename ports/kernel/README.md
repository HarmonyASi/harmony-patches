# HarmonyOS kernel interfaces for Aurora

`accesstokenid/` is based on the following pinned OpenHarmony `kernel_linux_5.10` `OpenHarmony-6.0-Release` commit:

`4e38b39c0ca8cc8768061c5ba645c1b748c66d95`

- `drivers/accesstokenid/access_tokenid.c`
- `drivers/accesstokenid/access_tokenid.h`

The original GPL-2.0 license and copyright notices are retained. The port explicitly includes modern kernel cred/uaccess headers and defines the platform's nwebspawn UID (3081) in this driver.

`ohos-access-token.patch` applies the official token/ftoken fields and Binder caller-identity propagation to the project's pinned Aurora source. It includes feature, access-token, and sender-info ioctls. Unlike the older L410 probe shim, this directly modifies source and does not depend on internal function addresses or kretprobe. Compliance with the complete HarmonyOS security policy still requires separate acceptance.

First check the patch against the pinned source, then copy the driver directory to `drivers/accesstokenid/` and enable `CONFIG_ACCESS_TOKENID=y`. Apply these steps only to a separate test-kernel build tree. The kernel and modules used for native boot must come from the same build; do not load old Kirin modules.
