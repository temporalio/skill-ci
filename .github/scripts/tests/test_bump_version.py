import textwrap
import unittest

from bump_version import get_next_version, set_json_version, set_version


def fixture(s: str) -> str:
    return textwrap.dedent(s).strip()


class TestGetNextVersion(unittest.TestCase):
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


class TestSetJsonVersion(unittest.TestCase):
    def test_update_version(self):
        src = fixture("""
            {
              "name": "temporal",
              "version": "0.4.0",
              "description": "lifecycle — developing"
            }
            """)
        expected = fixture("""
            {
              "name": "temporal",
              "version": "0.4.1",
              "description": "lifecycle — developing"
            }
            """)
        self.assertEqual(set_json_version(src, "0.4.1"), expected)

    def test_rejects_non_object(self):
        with self.assertRaises(ValueError):
            set_json_version("[]", "1.0.0")


class TestSetVersion(unittest.TestCase):
    def test_update_version(self):
        src = fixture("""
            ---
            name: temporal-developer
            description: The Temporal Developer skill
            version: 0.5.0
            ---
            """)
        expected = fixture("""
            ---
            name: temporal-developer
            description: The Temporal Developer skill
            version: 0.5.1
            ---
            """)
        self.assertEqual(set_version(src, "0.5.1"), expected)

    def test_preserves_formatting(self):
        src = (
            "---\n"
            "name: temporal-ops\n"
            "description: 'A long description that must remain on one line.'\n"
            "version: 0.2.0\n"
            "disable-model-invocation: true\n"
            "---\n"
            "\n"
            "# Skill\n"
        )
        expected = src.replace("version: 0.2.0", "version: 0.2.1")

        self.assertEqual(set_version(src, "0.2.1"), expected)

    def test_preserves_crlf_and_missing_final_newline(self):
        src = "---\r\nname: temporal-serverless\r\nversion: 0.6.0\r\n---"
        expected = src.replace("0.6.0", "0.6.1")

        self.assertEqual(set_version(src, "0.6.1"), expected)

    def test_rejects_missing_frontmatter(self):
        with self.assertRaises(ValueError):
            set_version("# Skill\n", "1.0.0")


if __name__ == "__main__":
    unittest.main()
