# Aurora + HarmonyOS Mac desktop development preview

This package was accepted against the user's criterion of reaching the desktop and opening application windows. See the package's `evidence` for actual results; commercial activation, in-app functionality, and native Apple hardware are outside that conclusion.

Requirements: Apple Silicon macOS, Python 3, QEMU, and lsof. Defaults are 4 GiB RAM, 4 vCPUs, 1920×1200 display, relative mouse, virtual keyboard, and user-mode networking.

1. In the package directory, run `shasum -a 256 -c SHA256SUMS`.
2. Run `python3 start.py --window` to open a macOS window; the setup wizard is automatically ended after about 120 seconds to reach the desktop. Use `--dry-run` to inspect the configuration. Without `--window`, it runs in headless diagnostic mode.
3. The launcher prints the `runs` directory. Wait for `LOCAL_ROOT_INTERACTIVE_READY` in `serial.log`. Run guest commands with `python3 tools/guest-console.py RUN 'command'`.
4. Run `python3 stop.py RUN` for a clean, synchronized shutdown and wait for the launcher to exit.
5. Export logs and screenshots with `python3 collect.py RUN evidence.tar.gz`.
6. After shutdown, run `python3 rollback.py` to inspect the rollback plan; `--apply` archives the old writable layer and creates a clean one while retaining the VM UUID.

`rootfs.qcow2` is the separate base disk; startup creates a persistent layer at `runtime/system.qcow2`. Do not start the same run disk concurrently or open it with another tool.

Known limitations: the desktop wallpaper is black and some icons are incomplete; Gallery stays on its first-use page, Browser was only verified to open a window, and File Manager exits. The startup script ends OOBE by calling the original `aa force-stop` after 116 seconds, so OOBE may briefly appear. Commercial `socIdCert`/TEE failure remains and does not count as activation. Absolute Tablet coordinates are unverified; use a relative mouse.

This package runs only on virtual hardware, with the test7 kernel and OHOS ABI llvmpipe. It has not accessed U393 or modified EFI/m1n1/GRUB. The Apple internal display, GPU, and built-in input require separate native validation.
