# Aurora + HarmonyOS local development preview

This is a macOS/HVF and UTM build-validation artifact. The complete desktop, basic applications, vendor hardware activation, and behavior on native Apple hardware have not completed acceptance; use the package's `manifest.json` qualification and corresponding evidence as the authority.

Requirements: Apple Silicon macOS, Python 3, QEMU (including `qemu-img` and `qemu-system-aarch64`), and lsof. Defaults are 4 GiB RAM, 4 vCPUs, 1920×1200 virtio display, virtual keyboard/mouse, and QEMU user-mode networking.

1. Verify: `shasum -a 256 -c SHA256SUMS`.
2. Inspect the launch command: `python3 start.py --dry-run`.
3. Start: `python3 start.py`. It creates a persistent writable layer at `runtime/system.qcow2` and leaves the separate `rootfs.qcow2` base image unchanged.
4. Wait for `LOCAL_ROOT_INTERACTIVE_READY` in the `serial.log` under the corresponding `runs` directory. Then use the temporary diagnostic port with `python3 tools/guest-console.py RUN 'command'`. Capture the screen with `python3 tools/guest-pointer.py RUN --capture frame.ppm`. Absolute Tablet pointer coordinates are not calibrated; use the original UITest for coordinate input.
5. Shut down cleanly with `python3 stop.py RUN`. Do not mount or modify the run disk until guest poweroff has been confirmed.
6. Collect logs with `python3 collect.py RUN evidence.tar.gz`.
7. Roll back by stopping the VM, running `python3 rollback.py` to inspect the plan, then `python3 rollback.py --apply`; the old writable layer is retained as an archive.

By default, the original HarmonyOS init/PID 1 and system services run. Debian is used only for building. Diagnostic services, virtual networking, and evidence markers are development-preview configuration.

The original setup wizard has not completed vendor activation. A newer test7/llvmpipe candidate passed preflight for actual JIT, pixels, the original queue, and wizard-page refresh. After DCM connected, the SoC-attestation request failed during TEEC initialization and could not obtain `socIdCert`. The exact kernel, renderer, and qualification scope are in `manifest.json` and the evidence. The package contains no vendor private key or activated identity; production security policy and native peripherals still need acceptance.

This package does not read or write U393, EFI, m1n1, or GRUB. `kernel/native-<test6-or-test7>-package.tar.zst` contains matching configuration and modules/DTBs handoff materials; native deployment requires separately checking machine identity, partitions, and boot rollback.

A newer test7 integrated preview creates and stores a UUID for the VM instance in `runtime/virtual-machine.json`; normal restarts and rollback retain it. The original init computes UDID from the actual virtual disk serial. Use a separate runtime directory for each VM instance; do not copy another device identity. `--dry-run` does not create an identity or run disk. The package's kernel, initrd, and modules are a validated fixed set and must not be mixed.
