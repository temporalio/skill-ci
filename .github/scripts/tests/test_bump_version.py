import unittest

from bump_version import set_json_version
from next_version import get_next_version


class TestGetNextVersion(unittest.TestCase):
    def test_initial_version(self):
        for strategy in ("patch", "minor", "major"):
            with self.subTest(strategy=strategy):
                self.assertEqual(get_next_version("", strategy), "0.1.0")

    def test_next_version(self):
        cases = (
            ("v0.0.0", "patch", "0.0.1"),
            ("v0.0.0", "minor", "0.1.0"),
            ("v1.2.3", "patch", "1.2.4"),
            ("v1.2.3", "minor", "1.3.0"),
            ("v1.2.3", "major", "2.0.0"),
        )

        for tag, strategy, expected in cases:
            with self.subTest(tag=tag, strategy=strategy):
                self.assertEqual(get_next_version(tag, strategy), expected)

    def test_rejects_invalid_tag(self):
        with self.assertRaises(ValueError):
            get_next_version("not-a-version", "patch")

    def test_rejects_invalid_strategy(self):
        with self.assertRaises(ValueError):
            get_next_version("", "latest")


class TestSetJsonVersion(unittest.TestCase):
    def test_update_version(self):
        src = '{"name":"temporal","version":"0.4.0","description":"lifecycle — developing"}'
        expected = """{
  "name": "temporal",
  "version": "0.4.1",
  "description": "lifecycle — developing"
}"""
        self.assertEqual(set_json_version(src, "0.4.1"), expected)

    def test_rejects_non_object(self):
        with self.assertRaises(ValueError):
            set_json_version("[]", "1.0.0")


if __name__ == "__main__":
    unittest.main()
