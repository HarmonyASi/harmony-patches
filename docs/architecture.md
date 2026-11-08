# Architecture

## Runtime environment

The boot chain consists of Apple platform boot components, m1n1/UEFI/GRUB, the Aurora kernel, and a separate initramfs. The initramfs loads the matching Apple drivers, locates the HarmonyOS root partition, and then uses `switch_root` to start the original `/system/bin/init`.

The target user space uses HarmonyOS's own parameter service, SAMgr, HDF, Foundation, RenderService, SceneBoard, and MMI. Debian/UTM is used for building, diagnostics, and recovery.

## Kernel adaptation

The pinned Aurora baseline and OpenHarmony sources are listed in [source-lock.json](../ports/kernel/source-lock.json). The main work includes:

- Supporting HarmonyOS's 4 KiB user-page contract with a 16 KiB kernel page size.
- Handling Binder mapping boundaries and native page allocation.
- AccessToken/ftoken identity fields and Binder identity propagation.
- An ashmem compatibility module.
- User-page policy after `exec` and BPF ring-buffer user mappings.

The kernel, modules, device tree, and initramfs must come from the same build. Native tools still pin the `test7` name and must be rechecked when upgrading.

## Software display path

Application/RenderService → OHOS EGL/NativeWindow bridge → Mesa llvmpipe → original buffer queue → HDF allocator/composer → DRM/KMS → Apple display driver.

`buffer_vdi.cpp` allocates DRM dumb/PRIME buffers; `egl_window_bridge.cpp` transfers pixels between Mesa GBM and the HarmonyOS NativeWindow queue; `composer.cpp` copies the client-composed target into persistent scanout buffers and submits them to KMS. All layers currently fall back to CLIENT composition; there is no hardware overlay or cursor acceleration.

The platform C++ boundary uses the original `std::__h` / `libc++.so`; SDK `std::__n1` objects do not cross that boundary. The pinned image uses a 56-byte BufferHandle ABI, which cannot be replaced directly with the public API 20 64-byte layout.

On native hardware with a display node but no renderD node, the current llvmpipe path requires `GBM_ALWAYS_SOFTWARE=1`; setting only `LIBGL_ALWAYS_SOFTWARE` does not select the GBM software path.

## Native boot notes

An external USB-C root disk depends on the Type-C device graph, and the display driver provides some route providers. Loading `appledrm` only after mounting the root disk creates a boot-order dependency, so the native bootstrap loads related display modules before searching for the root disk. The PMP driver must also be in the initramfs and loaded before `appledrm`.

The retained native scripts contain historical root UUID, exact kernel-version, and log-target constraints. They correspond to a specific validation baseline and must be reviewed before moving to another machine; see [Running and native boot](running.md).

## L410 reference boundary

The initial reference material came from L410 HarmonyOS adaptation work. The Kirin/Mali, amplifier, fingerprint, and Linux application-compatibility implementations were not copied wholesale into this repository. Apple-platform kernel, allocator/composer, and EGL bridge work is under `ports/` and does not depend on an external `l410/` source directory. System libraries in the original image remain external build inputs.
