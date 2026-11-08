# Running and native boot

## macOS development preview

`ports/release/` contains source for the preview-package tools and requires a matching image, kernel, initrd, and manifest. The image download link is maintained in the root README.

With a complete preview package, run these commands from the **preview package directory**:

```sh
shasum -a 256 -c SHA256SUMS
python3 start.py --dry-run
python3 start.py --window
```

Requirements are Apple Silicon macOS, QEMU, Python 3, and lsof. Follow the specific package README and manifest: a standard preview and a direct-desktop candidate have different startup behavior.

The launcher creates a persistent writable layer at `runtime/system.qcow2` and run records. Do not open the same run disk concurrently. Use `python3 stop.py RUN` to request a clean shutdown, and confirm the VM has exited before mounting or modifying the disk. `collect.py` gathers run records; `rollback.py` displays a rollback plan by default and only applies it with `--apply`.

The diagnostic console, virtual networking, and OOBE completion are development configuration. A direct-desktop candidate reaching the desktop after ending the wizard does not mean the device is activated; some applications have only been verified to open a window.

## Native deployment

This repository does not provide a one-click installer for arbitrary machines. The retained native scripts correspond to the existing J514S/test7 validation baseline:

- `initramfs/native-stage-init` pins the historical root UUID and kernel version, defaults to read-only rescue, and also requires a rootfs preparation marker in boot mode.
- `initramfs/native-log-collect` contains the original test environment's log destination and device constraints; review and adapt it before use.
- `tools/populate-rootfs.sh` writes to an already mounted standalone ext4 filesystem. Its default UUID is the original test partition; explicitly pass the actual UUID for any other target.
- `tools/adapt-local-root.py` and the service configuration tools modify an offline rootfs. Do not point them at a running system root.

The original U393 GPT/partition-rearrangement script is not included, nor are personal EFI, GRUB, or m1n1 backups. Porters need a separate root partition, matching firmware, and a boot entry with a rollback path, and must recheck disk identity, UUIDs, and fixed script parameters for their machine.

The original L410 ISO installer erases the entire target disk and must not be used as an installation method for Apple hardware or an existing partition layout. The build process only uses read-only extracted payloads.

## Logs and reports

The bootstrap can save logs after a native boot failure. The current implementation prefers an external test disk, and its fallback log destination includes the internal ESP. Check the destination before adopting this mechanism. Remove device identifiers, personal paths, network addresses, and account information before sharing reports.

When reporting a problem, include the model, source commit, image/kernel version, whether the run was native or HVF, reproduction steps, and the actual display result and relevant logs. Record firmware loading, service readiness, and desktop visibility as separate milestones.
