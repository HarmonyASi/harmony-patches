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

- `initramfs/native-stage-init` reads the root UUID, kernel release, and ordered early-module lists from the matching generated device profile. The default profile preserves the historical J514S/test7 values; J293 remains an unqualified candidate and cannot produce an initramfs until its matching values and artifacts exist. Rescue remains the default, and boot mode also requires a rootfs preparation marker.
- `initramfs/native-log-collect` contains the original test environment's log destination and device constraints; review and adapt it before use.
- `tools/populate-rootfs.sh` writes to an already mounted standalone ext4 filesystem. Its default UUID is the original test partition; explicitly pass the actual UUID for any other target.
- `tools/adapt-local-root.py` and the service configuration tools modify an offline rootfs. Do not point them at a running system root.

The original U393 GPT/partition-rearrangement script is not included, nor are personal EFI, GRUB, or m1n1 backups. Porters need a separate root partition, matching firmware, and a boot entry with a rollback path, and must recheck disk identity, UUIDs, and fixed script parameters for their machine.

### J293 boot-path proposal: not verified

The repository describes the general Apple platform → m1n1/UEFI/GRUB → Aurora kernel/initramfs chain, but contains no J293 boot entry, Fedora GRUB configuration, or Fedora installation procedure. The only recorded native root-disk result is for J514S using an external USB-C disk. It does not establish how this J293 Fedora installation boots or which boot manager/configuration it uses.

Do not assume macOS can mount or safely modify the Fedora ext4 filesystem; that depends on the macOS version and separately installed filesystem support, neither of which is established here. Likewise, a Fedora GRUB menu entry is not proven to be isolated from the existing boot path or guaranteed not to prevent normal boot. Its effect and recovery behavior depend on the actual firmware boot selection, EFI files, GRUB installation/configuration, entry placement, kernel/DTB/initramfs paths, and fallback configuration.

Before considering such a setup, identify the currently active boot path and its owner, confirm where its configuration and EFI files reside, establish a tested recovery route, and determine how the relevant ext4 files can be accessed without risking the Fedora system. J293 still has no qualified HarmonyOS root filesystem, root UUID, or initramfs; the recorded kernel and DTB evidence is compile-only. No partition, EFI, GRUB, or other bootloader changes were performed as part of this work.

The original L410 ISO installer erases the entire target disk and must not be used as an installation method for Apple hardware or an existing partition layout. The build process only uses read-only extracted payloads.

## Logs and reports

The bootstrap can save logs after a native boot failure. The current implementation prefers an external test disk, and its fallback log destination includes the internal ESP. Check the destination before adopting this mechanism. Remove device identifiers, personal paths, network addresses, and account information before sharing reports.

When reporting a problem, include the model, source commit, image/kernel version, whether the run was native or HVF, reproduction steps, and the actual display result and relevant logs. Record firmware loading, service readiness, and desktop visibility as separate milestones.
