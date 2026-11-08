#!/usr/bin/env python3
"""Load and validate native hardware profiles for initramfs builds."""
import json
import re
import uuid
from pathlib import Path


PROFILE_PATH = Path(__file__).resolve().parents[1] / 'config/native-device-profiles.json'
REQUIRED_BUILD_INPUTS = (
    'kernel_release',
    'root_uuid',
    'module_seed',
    'pre_root_modules',
    'pre_root_display_modules',
)


def load_profiles():
    return json.loads(PROFILE_PATH.read_text())


def get_profile(name):
    profiles = load_profiles()
    if name not in profiles:
        raise ValueError(f"Unknown native device profile '{name}'")
    profile = profiles[name]
    profile['id'] = name
    return profile


def require_build_inputs(profile):
    missing = [key for key in REQUIRED_BUILD_INPUTS if not profile.get(key)]
    if missing:
        raise ValueError(
            f"Native device profile '{profile['id']}' is not build-qualified; "
            f"required inputs are missing: {', '.join(missing)}"
        )
    if not re.fullmatch(r'[A-Za-z0-9._+-]+', profile['kernel_release']):
        raise ValueError(f"Invalid kernel release in native device profile '{profile['id']}'")
    try:
        uuid.UUID(profile['root_uuid'])
    except ValueError as exc:
        raise ValueError(f"Invalid root UUID in native device profile '{profile['id']}'") from exc
    for key in ('module_seed', 'pre_root_modules', 'pre_root_display_modules'):
        values = profile[key]
        if not isinstance(values, list) or not values or \
                any(not isinstance(module, str) or
                    not re.fullmatch(r'[A-Za-z0-9._+-]+', module) for module in values):
            raise ValueError(f"Invalid {key} in native device profile '{profile['id']}'")
    return profile
