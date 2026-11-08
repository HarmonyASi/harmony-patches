#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))

from native_device_profiles import get_profile, require_build_inputs


class NativeDeviceProfilesTest(unittest.TestCase):
    def test_j514s_profile_preserves_test7_build_inputs(self):
        profile = require_build_inputs(get_profile('j514s'))
        self.assertEqual(profile['kernel_release'], '7.2.11-aurora-hmos-j514s-test7')
        self.assertEqual(profile['root_uuid'], 'de5b04b6-597d-4382-b6a3-9e04388ccd6d')
        expected_modules = (
            'pinctrl-apple-gpio gpio-shared-proxy spi-apple i2c-pasemi-platform '
            'spmi-apple-controller apple_nvmem_spmi macsmc gpio-macsmc sn201202x '
            'tps6598x phy-apple-atc dwc3-apple thunderbolt_apple onboard_usb_dev '
            'mux-apple-display-crossbar phy-apple-dptx typec_displayport apple-sart '
            'nvme-apple apple-rtkit-helper apple-sio apple-dockchannel dockchannel-hid '
            'spi-hid-apple-of hid-apple hid-magicmouse hid-multitouch macsmc-input '
            'apple-pmp appledrm'
        ).split()
        self.assertEqual(profile['module_seed'], expected_modules)
        self.assertEqual(profile['module_seed'],
                         profile['pre_root_modules'] + profile['pre_root_display_modules'])

    def test_j293_is_identified_but_not_build_qualified(self):
        profile = get_profile('j293')
        self.assertEqual(profile['model'], 'Apple MacBook Pro (13-inch, M1, 2020)')
        self.assertEqual(profile['soc'], 'T8103')
        self.assertEqual(profile['device_tree_compatibles'], ['apple,j293', 'apple,t8103'])
        self.assertEqual(profile['status'], 'candidate-unqualified')
        self.assertEqual(
            profile['kernel_compile_evidence']['status'],
            'compile-only-not-boot-tested',
        )
        self.assertEqual(
            profile['kernel_compile_evidence']['source_commit'],
            'd13466ebb8b5f2e2af3d2c8359f4c96e711a5679',
        )
        self.assertIsNone(profile['kernel_release'])
        self.assertIsNone(profile['root_uuid'])
        self.assertIsNone(profile['module_seed'])
        with self.assertRaisesRegex(
            ValueError,
            'kernel_release, root_uuid, module_seed, pre_root_modules, pre_root_display_modules',
        ):
            require_build_inputs(profile)

    def test_j293_builder_fails_before_creating_output(self):
        builder = TOOLS / 'build-native-initramfs.py'
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / 'candidate-output'
            result = subprocess.run(
                [
                    sys.executable, str(builder), '--device-profile', 'j293',
                    '--modules', 'unused', '--bootstrap', 'unused', '--firmware', 'unused',
                    '--ext4-uuid', 'unused', '--kernel-log', 'unused', '--fat-uuid', 'unused',
                    '--output', str(output),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('not build-qualified', result.stderr)
            self.assertIn('kernel_release, root_uuid, module_seed', result.stderr)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
