import argparse

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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("tag", help="The current release tag, or an empty string")
    parser.add_argument("strategy", help="The package strategy")
    args = parser.parse_args()
    print(get_next_version(args.tag, args.strategy))


if __name__ == "__main__":
    main()
