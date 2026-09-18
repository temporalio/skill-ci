import argparse
import json
from pathlib import Path

from next_version import get_next_version


def set_json_version(text: str, version: str) -> str:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("plugin.json must be a JSON object")
    data["version"] = version
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="Path to plugin.json")
    parser.add_argument("tag", help="The current tag")
    parser.add_argument("strategy", help="The package strategy")
    args = parser.parse_args()

    new_version = get_next_version(args.tag, args.strategy)
    text = args.path.read_text(encoding="utf-8", newline="")
    updated = set_json_version(text, new_version)
    args.path.write_text(updated, encoding="utf-8", newline="")
    print(new_version)


if __name__ == "__main__":
    main()
