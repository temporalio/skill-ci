import argparse
import json
import re
from pathlib import Path

import semver


FRONTMATTER = re.compile(
    r"\A---\r?\n(?P<body>.*?)(?=\r?\n---(?:\r?\n|\Z))",
    re.DOTALL,
)
VERSION = re.compile(
    r"^version[ \t]*:[ \t]*"
    r"(?P<value>\"[^\r\n\"]*\"|'[^\r\n']*'|[^\s#'\"]+)"
    r"(?=[ \t]*(?:#[^\r\n]*)?\r?$)",
    re.MULTILINE,
)


def get_next_version(tag: str, strategy: str) -> str:
    version = semver.Version.parse(tag.removeprefix("v"))
    return str(version.next_version(strategy))


def set_version(text: str, version: str) -> str:
    frontmatter = FRONTMATTER.match(text)
    if frontmatter is None:
        raise ValueError("SKILL.md must start with YAML frontmatter")

    matches = list(VERSION.finditer(frontmatter["body"]))
    if len(matches) != 1:
        raise ValueError("SKILL.md frontmatter must contain exactly one version")

    match = matches[0]
    current = match["value"]
    quote = current[0] if current[0] in "\"'" else ""
    replacement = f"{quote}{version}{quote}"
    start = frontmatter.start("body") + match.start("value")
    end = frontmatter.start("body") + match.end("value")
    return text[:start] + replacement + text[end:]


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
    text = args.path.read_bytes().decode("utf-8")
    if args.path.suffix == ".json":
        updated = set_json_version(text, new_version)
    else:
        updated = set_version(text, new_version)
    args.path.write_bytes(updated.encode("utf-8"))
    print(new_version)


if __name__ == "__main__":
    main()
