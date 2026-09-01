import argparse

import semver


def validate_rollback_version(version: str) -> None:
    if not version:
        raise ValueError("rollback_version is required when package_strategy is rollback")
    semver.Version.parse(version)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("version", help="The rollback version")
    args = parser.parse_args()
    validate_rollback_version(args.version)


if __name__ == "__main__":
    main()
