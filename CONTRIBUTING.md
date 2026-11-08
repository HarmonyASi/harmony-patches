# Contributing

See the [build guide](docs/build.md) for development entry points and the [status guide](docs/status.md) for verification boundaries. When adding a device or image, record the exact hardware, dependency commits, kernel configuration, artifact hashes, and scope of hands-on testing.

Before submitting changes, run:

```sh
python3 scripts/check-repository.py
```

The check covers file sizes, generated artifacts, common private-key/token patterns, personal absolute paths, relative documentation links, Python syntax, and shell syntax. It does not build the system, access a device, or run boot or deployment scripts.

The per-file size limit is 1 MiB and the repository content limit is 10 MiB. If source genuinely needs to exceed a limit, adjust the check and explain why; images and build artifacts are provided through the Baidu Netdisk link in the README. Keep raw logs and chat records local, and include only necessary, redacted excerpts in reports.

Behavior changes should include targeted validation and distinguish virtual tests, native-hardware tests, and hypotheses. Documentation or source cleanup does not count as re-validating the system.

Original contributions are released under GPL-3.0-only. Preserve copyright and license notices when bringing in upstream files, and update the third-party source documentation.
