import argparse
import json
from pathlib import Path

import semver


INITIAL_VERSION = "0.1.0"
VERSION_STRATEGIES = {"patch", "minor", "major"}


def get_next_version(tag: str, strategy: str) -> str:
    if strategy not in VERSION_STRATEGIES:
        raise ValueError(f"Unsupported version strategy: {strategy}")
    if not tag:
        return INITIAL_VERSION
    version = semver.Version.parse(tag.removeprefix("v"))
    return str(version.next_version(strategy))


def set_json_version(text: str, version: str) -> str:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("plugin.json must be a JSON object")
    data["version"] = version
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, nargs="?", help="Path to plugin.json to update")
    parser.add_argument("tag", help="The current release tag, or an empty string")
    parser.add_argument("strategy", help="The package strategy")
    args = parser.parse_args()

    new_version = get_next_version(args.tag, args.strategy)
    if args.path:
        text = args.path.read_text(encoding="utf-8", newline="")
        updated = set_json_version(text, new_version)
        args.path.write_text(updated, encoding="utf-8", newline="")
    print(new_version)


if __name__ == "__main__":
    main()
