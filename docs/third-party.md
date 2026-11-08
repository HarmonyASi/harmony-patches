# Third-party sources and licenses

Original code, scripts, and documentation in this repository are licensed under the root GPL-3.0-only license by default. Where a file has an upstream copyright, license, or SPDX notice, that file and upstream license take precedence. Kernel patches follow the licenses of the kernel files they modify; Mesa patches follow the licenses of their corresponding upstream files.

| Material | Source | License handling |
| --- | --- | --- |
| Aurora kernel patches | [omacom/linux-aurora](https://github.com/omacom/linux-aurora), `d13466ebb8b5f2e2af3d2c8359f4c96e711a5679` | Retains the license of the corresponding Linux files, generally GPL-2.0; the complete kernel is not copied |
| AccessToken driver and original comparison files | [OpenHarmony kernel_linux_5.10](https://github.com/openharmony/kernel_linux_5.10), `4e38b39c0ca8cc8768061c5ba645c1b748c66d95`, `drivers/accesstokenid/` | Retains Huawei copyright and GPL-2.0 notices; port changes are described in the kernel README |
| ashmem implementation and UAPI | `kernel/ashmem/` | Implementation is GPL-2.0-only; UAPI retains Google copyright and GPL-2.0 OR Apache-2.0 |
| Display IDL and interface headers | [OpenHarmony drivers_interface](https://github.com/openharmony/drivers_interface), `9eaf9abff9c3906f4bf95271cf482e72c3b8c29` | Retains Apache-2.0 and Huawei Device notices; translated structure headers retain Apache-2.0 notices |
| HDF loading protocol reference | [OpenHarmony drivers_peripheral](https://github.com/openharmony/drivers_peripheral), `8cd47d4bb09a4d160e8b713b2fbccf8d41e2025f` | Upstream protocol is referenced; target libraries are supplied by the external image |
| DFX dump catcher declarations | OpenHarmony DFX interface in `tests/include/dfx_dump_catcher.h` | Retains Apache-2.0 and Huawei Device notices; the original record does not pin a separate source commit |
| Mesa patches | Baseline `7c86130d26cecd50c7af1ac01ff3fa1705d58045` | Used under the corresponding Mesa file licenses; full copyright material is in the external source tree |
| LLVM, libdrm, zlib, expat, BusyBox | External build inputs | Source and binaries are not bundled; distribution of build artifacts requires retaining their licenses and corresponding source obligations |

Historical records list the `DisplayComposerType.idl` SHA256 as `8be06dca7cba51335a31d31c8f979e20ffa3dd8149b7ce181667f5bcb3dc41a0` and the drivers_peripheral codeload archive SHA256 as `372784383662527e8beea176a1290252efb3c50188e761db8a0e3fd64c2e89f3`.

The original development materials included L410 adaptation source and a GPL-3.0 license text; this repository does not include that complete work. Original HarmonyOS services, system libraries, SDKs, firmware, images, and commercial services are external materials; this repository's GPL license does not grant rights to redistribute them.

License texts: [GPL-3.0-only](../LICENSE), [GPL-2.0](../LICENSES/GPL-2.0-only.txt), [Apache-2.0](../LICENSES/Apache-2.0.txt).
