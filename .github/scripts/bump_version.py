import argparse
import json
from pathlib import Path

import semver


def get_next_version(tag: str, strategy: str) -> str:
    version = semver.Version.parse(tag.removeprefix("v"))
    return str(version.next_version(strategy))


def set_version(text: str, version: str) -> str:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter")

    version_lines = []
    for index, line in enumerate(lines[1:], start=1):
        content = line.rstrip("\r\n")
        if content == "---":
            break
        if content.startswith("version: "):
            version_lines.append(index)

    if len(version_lines) != 1:
        raise ValueError("SKILL.md frontmatter must contain exactly one version")

    index = version_lines[0]
    content = lines[index].rstrip("\r\n")
    newline = lines[index][len(content) :]
    lines[index] = f"version: {version}{newline}"
    return "".join(lines)


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
    text = args.path.read_text(encoding="utf-8", newline="")
    if args.path.suffix == ".json":
        updated = set_json_version(text, new_version)
    else:
        updated = set_version(text, new_version)
    args.path.write_text(updated, encoding="utf-8", newline="")
    print(new_version)


if __name__ == "__main__":
    main()
