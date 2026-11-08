# Initial plan for multi-device support

## Current baseline

The only documented native-hardware validation target is Apple M3 Pro / J514S. The existing native boot scripts, kernel release checks, root UUID, module list, display assumptions, and artifact packaging are tied to that test baseline. Other Apple Silicon models should be treated as unsupported until qualified. A device tree alone will not establish compatibility: boot firmware, kernel configuration, drivers, storage, display, input, and HarmonyOS service configuration also need to match.

The goal of the first phase is not to claim broad support, but to add a second, explicitly identified target without regressing J514S.

## First candidate: MacBook Pro (13-inch, M1, 2020) / J293

The supplied device tree identifies this machine as `apple,j293` and `apple,t8103`. Its model-specific nodes describe the internal panel/DCP path, Touch Bar, SPI HID input, I2C audio codecs, and `apple,honshu` Wi-Fi/Bluetooth board types. These are hardware-description evidence only; they do not establish that the current HarmonyMac kernel, initramfs, firmware, or HarmonyOS services support those components.

| Area | Evidence and current status |
| --- | --- |
| Identity | Identified by the supplied DTS as MacBook Pro (13-inch, M1, 2020), J293 / T8103. |
| Device tree | The pinned Aurora source tree contains `t8103-j293.dts`; J293 DTB compilation succeeded. The resulting DTB has not been tested in the HarmonyMac boot chain. |
| Kernel | Compile-only evidence: the pinned Aurora source built with the test7 config plus the five HarmonyMac kernel patches and `accesstokenid` source. The build was not boot-tested. |
| Modules | `modules_install` copied 1,005 modules (about 1.1 GB); `depmod` was unavailable, so module metadata is incomplete. This is an unfiltered install, not a qualified initramfs module set. |
| Storage and boot path | Not tested with HarmonyMac on J293. |
| Display and Touch Bar | DTS describes the J293 panel/DCP and Touch Bar; neither has been tested with HarmonyMac. |
| Input | DTS describes SPI HID input; it has not been tested with HarmonyMac. |
| Audio | DTS describes TI speaker codecs and a Cirrus jack codec; audio has not been tested with HarmonyMac. |
| Wi-Fi and Bluetooth | DTS identifies the `apple,honshu` board type. Matching HarmonyMac drivers and firmware have not been qualified. |
| HarmonyOS startup and services | Not tested on J293. |

The native initramfs builder now has explicit `j514s` and `j293` profiles. J514S retains its existing test7 kernel release, root UUID, module seed, and ordered early-module lists. J293 remains an unqualified candidate: its profile records compile-only evidence but intentionally lacks an adopted kernel release, root UUID, module seed, and ordered early-module lists, so selecting it fails before creating build output. This is code scaffolding, not J293 boot support. The rootfs population script's default UUID remains J514S-only; any future target must pass its verified expected UUID explicitly.

### J293 kernel compile evidence

- Source: `aurora-silicon/linux` commit `d13466ebb8b5f2e2af3d2c8359f4c96e711a5679`; that tree already contains `t8103-j293.dts`.
- Build inputs: historical `test7.config`, all five HarmonyMac kernel patches, and the HarmonyMac `accesstokenid` source.
- Build settings: `build-test-kernel.sh` suffix `-aurora-hmos-j293-test1`, LLVM 19, and GNU ld. LLD hit the build script's VDSO offset parser; GNU ld produced a successful build.
- Output evidence: kernel image about 26 MB and J293 DTB about 77 KB. The working tree was dirty, so the observed release was `7.2.11-aurora-hmos-j293-test1+`; this `+` release is not adopted as the profile's kernel release.
- Scope: compilation only; no boot, initramfs, root-device discovery, or J293 hardware validation. No J293 root UUID or persistence strategy has been selected. No binary artifacts or build config are checked into this repository.
- Module handoff: `modules_install` copied 1,005 modules (about 1.1 GB), but `depmod` was absent and generated module metadata is incomplete. This is not a curated or usable J293 initramfs module set.

An installed Fedora Asahi reference provides a J293 DTB and modules for Linux `6.19.13-400.asahi.fc44.aarch64+16k`; its config enables Apple-specific support including DART, SART, AOP, PMP, Apple DRM, NVMe, SPI, and HID. This is useful only as evidence that a separate Linux build has J293-specific configuration. Its kernel, DTB, modules, and firmware must not be mixed with HarmonyMac's pinned 7.2.11 baseline. Fedora files labeled `harmony` are excluded from this comparison.

Do not label J293 supported or change native boot defaults based on these references. Keep J514S as the known-good profile until a matching J293 kernel/initramfs set has been built and the qualification steps below pass on the machine.

## Proposed phases

1. **Collect a second-device hardware package.** Record the exact Mac model identifier, SoC generation, board/platform identifier if available, boot chain and firmware versions, kernel baseline/commit, and the intended HarmonyOS image/build. Gather the device tree (including overlays if relevant), kernel `.config`, matching modules and firmware inventory, and redacted boot logs. Keep serial numbers, account data, private paths, and other personal identifiers out of shared artifacts.
2. **Compare against J514S.** Identify differences in device-tree nodes, interrupt and power domains, clocks, regulators, GPIOs, storage topology, USB/Type-C routing, display/DCP, audio, and input. For each dependency, mark whether it is shared, model-specific, unavailable, or not yet tested. Do not infer support merely because both machines use Apple Silicon.
3. **Separate shared boot logic from per-device data.** The native initramfs now reads the kernel release, root UUID, and ordered early-module lists from its selected profile, while the builder preserves J514S's module seed and rejects profiles with missing build inputs. Extend this configuration only as verified J293 kernel, module/firmware, and root-device data become available. Keep J514S as the reference and fail clearly for unknown or incomplete profiles.
4. **Build a matching kernel/initramfs pair.** Apply only the required device-specific configuration and drivers. Ensure the kernel, modules, device tree, firmware, and initramfs are from one recorded build. Review early module-load ordering, root-disk discovery, display initialization, and log destinations for the target.
5. **Validate in increasing risk order.** First run static configuration and artifact checks; then boot to read-only rescue and confirm device discovery/root identity; next verify the display and input path; then start the original HarmonyOS init and core services; finally test persistence, peripherals, repeated cold boots, and stability. Keep virtual results separate from native results.
6. **Document support as a per-device matrix.** For every feature, record status as not tested, tested in VM, tested on hardware, or accepted, with the exact source commit, image, kernel, and evidence. Do not label a model supported based only on booting or reaching the desktop.

## Next J293 qualification inputs

The initial identity and DTS evidence are available. The next missing inputs are:

- macOS and boot-firmware versions, plus the intended HarmonyOS image/build.
- The kernel source commit, config, release string, modules, and firmware intended for the HarmonyMac J293 build.
- Which root-storage layout is intended for J293, and whether the HarmonyOS root must retain writable state across reboot; confirm the target filesystem and persistence behavior before assigning or recording any root UUID.
- A sanitized boot log from a known-good operating system and any Aurora attempt.
- Observed boot path, root-disk connection, display, keyboard/trackpad, and peripheral behavior on this machine.
- Any device configuration required by the HarmonyOS image that differs from J514S.

Do not send disk images, private keys, account credentials, or unredacted logs unless they are specifically needed and safe to share. Once the missing details are available, use them to identify which additional artifacts are necessary before attempting a J293 build.
