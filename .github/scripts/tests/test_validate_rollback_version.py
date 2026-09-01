import unittest

from validate_rollback_version import validate_rollback_version


class TestValidateRollbackVersion(unittest.TestCase):
    def test_accepts_valid_semver(self):
        cases = ("1.2.3", "1.2.3-alpha.1")
        for version in cases:
            with self.subTest(version=version):
                validate_rollback_version(version)

    def test_rejects_empty(self):
        with self.assertRaisesRegex(ValueError, "rollback_version is required"):
            validate_rollback_version("")

    def test_rejects_invalid_semver(self):
        cases = ("v1.2.3", "1.2", " 1.2.3")
        for version in cases:
            with self.subTest(version=version):
                with self.assertRaises(ValueError):
                    validate_rollback_version(version)


if __name__ == "__main__":
    unittest.main()
