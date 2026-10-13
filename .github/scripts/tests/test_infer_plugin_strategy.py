import unittest
from itertools import permutations

from infer_plugin_strategy import infer_plugin_strategy


class TestInferPluginStrategy(unittest.TestCase):
    def test_omitted_and_empty_inputs_do_not_bump(self):
        self.assertEqual(infer_plugin_strategy({}), "")
        self.assertEqual(
            infer_plugin_strategy({"skill-temporal-developer_package_strategy": ""}),
            "",
        )

    def test_largest_skill_bump_wins_regardless_of_order(self):
        cases = (
            (("", "", "", "patch"), "patch"),
            (("patch", "patch", "", "minor"), "minor"),
            (("patch", "major", "minor", ""), "major"),
            (("major", "major", "major", "major"), "major"),
        )
        for strategies, expected in cases:
            for ordered in set(permutations(strategies)):
                with self.subTest(strategies=ordered):
                    inputs = {
                        f"skill-example-{index}_package_strategy": strategy
                        for index, strategy in enumerate(ordered)
                    }
                    self.assertEqual(infer_plugin_strategy(inputs), expected)

    def test_rollback_requires_at_least_a_patch_bump(self):
        for strategy, expected in (("", "patch"), ("minor", "minor"), ("major", "major")):
            with self.subTest(strategy=strategy):
                inputs = {
                    "skill-temporal-developer_package_strategy": "rollback",
                    "skill-temporal-ops_package_strategy": strategy,
                }
                self.assertEqual(infer_plugin_strategy(inputs), expected)

    def test_only_skill_package_strategies_affect_the_bump(self):
        inputs = {
            "skill-temporal-developer_package_strategy": "patch",
            "skill-temporal-developer_rollback_version": "major",
            "claude-temporal-plugin_package_strategy": "major",
        }
        self.assertEqual(infer_plugin_strategy(inputs), "patch")

    def test_invalid_strategies_fail_even_if_another_skill_requests_major(self):
        for strategy in ("latest", "invalid", "Major", " patch "):
            with self.subTest(strategy=strategy):
                inputs = {
                    "skill-temporal-developer_package_strategy": "major",
                    "skill-temporal-ops_package_strategy": strategy,
                }
                with self.assertRaisesRegex(ValueError, "skill-temporal-ops_package_strategy"):
                    infer_plugin_strategy(inputs)


if __name__ == "__main__":
    unittest.main()
