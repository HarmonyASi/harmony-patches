# Build environment and process

This repository publishes development source and component tools; the process for rebuilding a complete image has not yet been assembled. This guide describes the scripts' actual inputs and known gaps. Cloning the repository and running every script will not produce an accepted system.

## Dependencies and versions

| Material | Recorded version / requirement |
| --- | --- |
| Aurora kernel | `omacom/linux-aurora`, `d13466ebb8b5f2e2af3d2c8359f4c96e711a5679` |
| OpenHarmony AccessToken | `kernel_linux_5.10`, `4e38b39c0ca8cc8768061c5ba645c1b748c66d95` |
| Mesa | `7c86130d26cecd50c7af1ac01ff3fa1705d58045` |
| OHOS toolchain | SDK 6.0.0.47 / API 20 sysroot; scripts refer to the Clang 15.0.4 resource directory |
| Linux build tools | Clang/LLVM 19, CMake, Meson, Ninja, pkg-config, readelf, patch |
| Target dependencies | OHOS ABI libdrm 2.4.124, zlib 1.3.1, expat 2.7.1, libc++; llvmpipe additionally needs target LLVM 19 |
| macOS virtual validation | Apple Silicon, QEMU AArch64/HVF, qemu-img, lsof, Python 3, Pillow |

Python tools use APIs such as `hashlib.file_digest` and `Path.is_relative_to`; Python 3.12 or later is recommended. The native builder needs a version that supports the `tarfile` data filter. SDK and graphics dependency hashes are in [graphics source locks](../ports/graphics/source-lock.json); the Mesa backend field records the earlier softpipe baseline.

The original system libraries, images, SDK, and firmware must be supplied by the developer. The original ISO reader targets `L410_INSTALL` and a fixed eight-part SquashFS layout; it does not support arbitrary HarmonyOS installation images.

## Toolchain and graphics

In a Linux build VM, prepare the external SDK, original rootfs, and a separate work directory. The following uses placeholder paths and only illustrates the tool order:

```sh
PROJECT="$PWD"
WORK=/path/to/build-work
SDK=/path/to/ohos-sdk
PLATFORM_ROOT=/path/to/original-root
mkdir -p "$WORK"
python3 ports/tools/prepare-ohos-toolchain.py \
  "$SDK" "$WORK/ohos-toolchain" \
  --prefix "$WORK/ohos-deps" --platform-root "$PLATFORM_ROOT"
```

First prepare OHOS ABI headers and libraries such as libdrm/zlib/expat under `ohos-deps/system`. `build-buffer-vdi.sh` and some probes still read platform libraries from the read-only original-image mount at `/mnt/harmonyos-source`; prepare that path as required by the scripts.

```sh
bash ports/tools/build-ohos-softpipe.sh /path/to/mesa "$WORK"
bash ports/tools/build-buffer-vdi.sh "$PROJECT" "$WORK"
bash ports/tools/build-composer.sh "$PROJECT" "$WORK"
bash ports/tools/build-egl-window-bridge.sh "$PROJECT" "$WORK"
```

llvmpipe uses a separate build prefix with `build-ohos-llvm.sh` and `build-ohos-llvmpipe.sh`. First copy `ports/tools/ohos-llvm19-toolchain.cmake` and `ohos-llvm-config.py` to the work-directory root, then build target LLVM. The CMake file locates the compiler under the adjacent `ohos-toolchain/` directory. The complete LLVM source lock and dependency build process are still missing; the softpipe command cannot simply be substituted for the llvmpipe command.

## Kernel and initramfs

In a separate build tree for the pinned Aurora source, inspect and apply the `kernel/` patches, add the `accesstokenid/` driver and its Kconfig/Makefile integration, and prepare an initial `.config` for the matching Apple machine before running `build-test-kernel.sh`. The script checks that existing Apple options have not been lost.

The historical [test7.config](../ports/kernel/test7.config) is included as a configuration reference for the same baseline. The patch application/driver integration script and module installation handoff are not yet complete. `kernel/ashmem/` is a separate module and must be built for the same kernel.

`build-native-initramfs.py --help` lists the required matching modules, static bootstrap, firmware, UUID utility, and output directory. The native builder is pinned to test7 and rejects missing modules or mismatched vermagic.

## Component validation

`tests/` contains graphics, Binder, page-interface, service-readiness, and input probes. `prepare-*-test.sh` builds the corresponding disk fixture, while `run-composer-vm.py` / `run-service-vm.py` run virtual preflight on macOS. Each fixture needs its matching kernel, modules, original services, and dependency closure.

Suggested order: page contract and IPC → allocator/composer → EGL and real NativeWindow queue → original init/HDF → RenderService → desktop/input → native hardware. Base conclusions on actual pixels, interaction, and logs; a successful script exit is not proof that every feature works.

## Preview packaging

`package-local-preview.py --help` describes the external disk, matching kernel/initrd/modules package, historical evidence, and output directory arguments. llvmpipe additionally requires explicit `--llvmpipe-evidence` and `--activation-evidence` arguments; it no longer accesses an old work directory implicitly.

The tool still checks fixed artifact hashes, root UUID, historical evidence filenames, and directory layout for packaging validated development candidates. Updating artifacts requires revalidation and updating those constraints. Packaging does not qualify a new image.
