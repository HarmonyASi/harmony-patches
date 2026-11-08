# Status and verification scope

Updated: 2026-11-07; development evidence through 2026-11-05. This page summarizes existing development records and user-reported tests. This documentation update did not reboot a VM or native device.

## Native hardware

The target hardware is Apple M3 Pro / J514S. Existing deployments use a separate HarmonyOS root partition, booted through the existing Apple/Aurora chain with a matching test7 kernel and initramfs.

| Area | Known result | Verification still needed |
| --- | --- | --- |
| External USB-C root disk | Native boot found and mounted the disk after display-route modules were loaded early | Other devices, ports, and machines |
| Internal display initialization | After adding the matching apple-pmp module, DCP initialized the display; recorded mode is 3024×1890@120 | Refresh timing, tearing, and performance |
| Original desktop and apps | User confirmed the desktop was visible and Settings opened | Full in-app behavior, local HAP installation, and persistence retest |
| Trackpad | User confirmed it works | Full keyboard input, gestures, and other input devices |
| Cursor trails | User reported severe trails; composer now synchronizes DMA-BUF writes to the target scanout buffer | Retest the fix on native hardware |
| Time to first image | User reported a black screen for about half a minute; monotonic frame-time logging has been added | Diagnose and fix the delay |
| Peripherals and stability | No complete acceptance result | Audio, wireless networking, Bluetooth, power management, multiple displays, repeated boots, and long-running use |

The display uses software rendering. A registered driver, successful application launch command, or registered service does not by itself prove that the image is visible or the feature works.

## Virtual component tests

Historical macOS/HVF test records include:

- Original HarmonyOS init/PID 1, SAMgr/HDF, and core service startup.
- test7 16 KiB kernel / 4 KiB user-page interfaces and Binder, ashmem, AccessToken, and BPF ring-buffer regression tests.
- Six original ConsumerSurface/NativeWindow buffer request, submit, consume, recycle, and pixel-check cycles.
- A minimal dynamic RenderService scene: two background color changes with pixel-exact comparison of 1280×800 scanout output.
- llvmpipe JIT and graphics queue component tests, preview startup, persistent overlay, clean shutdown, and rollback.
- A later direct-desktop candidate reaching the desktop and opening some application windows, with icon, wallpaper, and application behavior defects.

These results came from different test runs and fixed artifact combinations. They cannot be combined into a claim that an arbitrary image or the current source has passed full qualification. Original logs, frames, and disks remain in the development archive; this repository publishes only summaries and probe source.

## Activation and security policy

The original DCM reached HDI, but SoC attestation still fails during TEEC initialization and cannot obtain `socIdCert`. Ending OOBE in a development candidate does not mean commercial activation succeeded.

Historical tests used permissive SELinux and diagnostic service configuration. The production enforcing policy, permission isolation, and related security regression testing are not complete. Huawei accounts, cloud services, the app store, and vendor commercial activation are outside the confirmed basic port acceptance scope.

## Next steps

1. Retest the composer synchronization fix and determine whether cursor trails improve.
2. Use frame timing and boot logs to locate the first-image delay.
3. Complete reproducible handoff material for build dependencies, initial kernel configuration, and full service configuration.
4. For a specified release image, record input, application, HAP, persistence, and peripheral results individually.
