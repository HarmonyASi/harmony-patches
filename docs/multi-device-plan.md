# Initial plan for multi-device support

## Current baseline

The only documented native-hardware validation target is Apple M3 Pro / J514S. The existing native boot scripts, kernel release checks, root UUID, module list, display assumptions, and artifact packaging are tied to that test baseline. Other Apple Silicon models should be treated as unsupported until qualified. A device tree alone will not establish compatibility: boot firmware, kernel configuration, drivers, storage, display, input, and HarmonyOS service configuration also need to match.

The goal of the first phase is not to claim broad support, but to add a second, explicitly identified target without regressing J514S.

## Proposed phases

1. **Collect a second-device hardware package.** Record the exact Mac model identifier, SoC generation, board/platform identifier if available, boot chain and firmware versions, kernel baseline/commit, and the intended HarmonyOS image/build. Gather the device tree (including overlays if relevant), kernel `.config`, matching modules and firmware inventory, and redacted boot logs. Keep serial numbers, account data, private paths, and other personal identifiers out of shared artifacts.
2. **Compare against J514S.** Identify differences in device-tree nodes, interrupt and power domains, clocks, regulators, GPIOs, storage topology, USB/Type-C routing, display/DCP, audio, and input. For each dependency, mark whether it is shared, model-specific, unavailable, or not yet tested. Do not infer support merely because both machines use Apple Silicon.
3. **Separate shared boot logic from per-device data.** Replace hard-coded model-sensitive values with a small explicit device profile or build configuration, starting with model identity, kernel config, module/firmware set, and root-device selection. Keep the existing J514S profile as the reference and fail clearly for unknown profiles rather than silently using it.
4. **Build a matching kernel/initramfs pair.** Apply only the required device-specific configuration and drivers. Ensure the kernel, modules, device tree, firmware, and initramfs are from one recorded build. Review early module-load ordering, root-disk discovery, display initialization, and log destinations for the target.
5. **Validate in increasing risk order.** First run static configuration and artifact checks; then boot to read-only rescue and confirm device discovery/root identity; next verify the display and input path; then start the original HarmonyOS init and core services; finally test persistence, peripherals, repeated cold boots, and stability. Keep virtual results separate from native results.
6. **Document support as a per-device matrix.** For every feature, record status as not tested, tested in VM, tested on hardware, or accepted, with the exact source commit, image, kernel, and evidence. Do not label a model supported based only on booting or reaching the desktop.

## First target inputs

For the second model, the most useful initial handoff is:

- Exact model identifier and chip/board identity, plus the macOS and boot-firmware versions used for the test.
- Device tree and any overlays corresponding to the intended boot environment.
- Kernel source commit, `.config`, build release string, and matching modules/firmware list.
- A sanitized boot log from a known-good operating system, if available, and logs from any Aurora boot attempt.
- What you can already confirm: boot path, root-disk type/connection, internal display behavior, keyboard/trackpad, and whether the target is virtual or native.
- Exact HarmonyOS image/build and its existing device configuration, if it differs from the J514S image.

Do not send disk images, private keys, account credentials, or unredacted logs unless they are specifically needed and safe to share. Start with the device tree and the identifiers/version details above; we can then determine which additional artifacts are actually necessary.
