import argparse
import json
from pathlib import Path

import frontmatter
import semver


def get_next_version(tag: str, strategy: str) -> str:
    version = semver.Version.parse(tag.removeprefix("v"))
    return str(version.next_version(strategy))


def set_version(text: str, version: str) -> str:
    if not frontmatter.checks(text):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    post = frontmatter.loads(text)
    post["version"] = version
    return frontmatter.dumps(post, sort_keys=False)


def set_json_version(text: str, version: str) -> str:
    data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("plugin.json must be a JSON object")
    data["version"] = version
    return json.dumps(data, indent=2, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path, help="Path to SKILL.md or plugin.json")
    parser.add_argument("tag", help="The current tag")
    parser.add_argument("strategy", help="The package strategy")
    args = parser.parse_args()

    new_version = get_next_version(args.tag, args.strategy)
    text = args.path.read_text()
    if args.path.suffix == ".json":
        args.path.write_text(set_json_version(text, new_version))
    else:
        args.path.write_text(set_version(text, new_version))
    print(new_version)


if __name__ == "__main__":
    main()
