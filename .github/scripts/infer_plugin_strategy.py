import argparse
import json
from collections.abc import Mapping


BUMP_PRIORITIES = {"": 0, "patch": 1, "minor": 2, "major": 3}


def infer_plugin_strategy(inputs: Mapping[str, str]) -> str:
    plugin_strategy = ""
    for name, strategy in inputs.items():
        if not (name.startswith("skill-") and name.endswith("_package_strategy")):
            continue
        if strategy == "rollback":
            strategy = "patch"
        if strategy not in BUMP_PRIORITIES:
            raise ValueError(f"Unsupported package strategy for {name}: {strategy}")
        if BUMP_PRIORITIES[strategy] > BUMP_PRIORITIES[plugin_strategy]:
            plugin_strategy = strategy
    return plugin_strategy


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", help="Workflow dispatch inputs as JSON")
    args = parser.parse_args()
    print(infer_plugin_strategy(json.loads(args.inputs)))


if __name__ == "__main__":
    main()
