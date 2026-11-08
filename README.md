# HarmonyMac

Run the HarmonyOS user space on the Aurora Linux kernel for Apple Silicon.

HarmonyOS provides its own init, system services, SceneBoard desktop, input stack, and applications. Aurora provides the Linux kernel and Apple hardware drivers. Development and virtual preflight use macOS with UTM/QEMU; the target environment boots the HarmonyOS user space independently.

## Status

This is an experimental port. The currently documented native hardware validation is **Apple M3 Pro / J514S**; other models have not been verified. The status below is based on development records through 2026-11-05.

- The HarmonyOS desktop has appeared on native hardware; Settings opens and the trackpad works.
- The current graphics path uses Mesa llvmpipe with the OHOS ABI for software rendering; Apple GPU hardware acceleration is not connected.
- Native hardware has severe cursor trails and takes about half a minute to show the first image. A DMA-BUF synchronization fix in the composer has been deployed and passed a small frame-submission check; its effect on native hardware still needs re-testing.
- macOS/HVF has passed component-level checks for the original init, service chain, real graphics queue, and pixels. These results do not mean the complete system has passed acceptance.
- Huawei accounts, cloud services, the app store, and commercial device activation have not been verified. Commercial activation currently fails during TEE/SoC attestation; a development candidate can reach the desktop by ending OOBE.
- Audio, Wi-Fi, Bluetooth, sleep, multiple displays, and long-term stability have not completed native-hardware acceptance.

See [Status and verification scope](docs/status.md) for detailed progress and [Architecture](docs/architecture.md) for implementation details.

## Image download

HarmonyOS images are available through [Baidu Netdisk](https://pan.baidu.com/s/1DmrbZjC8IqnzeOEG4j0vOg?******).

The image version, SHA256, and corresponding source commit still need to be recorded.

This repository contains only adaptation source, patches, and documentation. It does not include ISOs, root filesystems, virtual disks, kernel binaries, modules, firmware, SDKs, or runtime logs.

## Development docs

- [Build environment and process](docs/build.md): dependencies, pinned versions, script entry points, and reproducibility gaps.
- [Running and native boot](docs/running.md): preview-package usage and native deployment boundaries.
- [Third-party sources and licenses](docs/third-party.md): upstream materials from Aurora, OpenHarmony, Mesa, and others.
- [Multi-device support plan](docs/multi-device-plan.md): an initial plan and the hardware details needed to qualify another Mac.
- [Contributing and repository checks](CONTRIBUTING.md).

```text
ports/
├── kernel/      # Kernel patches, AccessToken, and ashmem
├── graphics/    # DRM allocator/composer, EGL bridge, and Mesa patches
├── initramfs/   # Boot, module loading, and automatic log collection
├── config/      # HDF configuration
├── tools/       # Build, rootfs adaptation, and virtual validation tools
├── tests/       # Interface, service, graphics, and input probes
└── release/     # Development preview start, stop, log collection, and rollback tools
```

## License

Original code, scripts, and documentation in this project are licensed under [GPL-3.0-only](LICENSE). Third-party files and upstream-derived materials retain their own licenses; see [Sources and licenses](docs/third-party.md). This repository's license does not grant rights to HarmonyOS images or third-party binaries.
