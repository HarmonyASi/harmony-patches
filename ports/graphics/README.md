# Aurora HarmonyOS display backend

The current path uses Mesa software rendering with the OHOS ABI, the original NativeWindow queue, and DRM/KMS output. See [status](../../docs/status.md) for the latest native-hardware state and the [build guide](../../docs/build.md) for build entry points.

## Components

- `drm_device.c` enumerates DRM cards, ignores simpledrm, and prefers appledrm and the internal display.
- `buffer_vdi.cpp` allocates linear RGBA/RGBX/BGRA/BGRX dumb/PRIME buffers, fills in `BufferHandle.virAddr` as required by the original HDI, and rejects protected buffers.
- `composer.cpp` falls back to CLIENT composition for all layers, copies the client target into persistent double buffers, synchronizes CPU writes to DMA-BUF, and submits to KMS. It waits for page flips and retains pending state on timeout.
- `egl_window_bridge.cpp` loads OHOS Mesa EGL from a separate `libEGL_impl.so`, preserves GLES default-framebuffer semantics with a GBM backing surface, and converts/submits pixels to the HarmonyOS queue on swap. Backing surfaces are created lazily using the actual geometry.
- `patches/` contains Mesa profiler overhead fixes, resource-release fixes, and bounded-draw diagnostics. Diagnostic patches are optional.

## ABI and tests

The platform boundary uses the original `std::__h` and `libc++.so`; SDK `std::__n1` objects do not cross it. `buffer_handle.h` defines a 56-byte internal ABI for the pinned image and cannot be replaced with the 64-byte API 20 layout.

Build entry points are under `../tools/`: `build-buffer-vdi.sh`, `build-composer.sh`, and `build-egl-window-bridge.sh`. Tests are under `../tests/` and cover allocator/composer, EGL, the original queue, RenderService, and VSync.

## Limitations

The current implementation supports one connector and its preferred mode, without hardware overlay/cursor, HDR, or complete hotplug handling. VSync is scheduled from the selected mode and is not locked to hardware vblank. CPU-copy performance, multithreading, multiple windows, and cross-process metadata semantics need further verification. Native cursor trails and time-to-first-image have not completed fix acceptance.

Interface sources and pinned commits are listed in [Third-party sources and licenses](../../docs/third-party.md).
