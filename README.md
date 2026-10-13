# skill-ci

A Temporal plugin release spans several skill and plugin repositories. This repo is the CI that coordinates that work. Dispatch **Plugin Release** here to ship new content across:

Skills:

- `skill-temporal-cloud-setup`
- `skill-temporal-developer`
- `skill-temporal-ops`
- `skill-temporal-serverless`

Plugins:

- `claude-temporal-plugin`
- `codex-temporal-plugin`
- `cursor-temporal-plugin`

## Releasing new versions

Each skill's package strategy is optional. Leave it blank for no bump, or enter
`patch`, `minor`, `major`, or `rollback`.

| Skill strategy | Effect |
|----------------|--------|
| `patch` / `minor` / `major` | Calculate the next version, create a GitHub Release for the current validated `main` commit, and use this new release |
| Omitted | Use the latest release instead of releasing a new skill version |
| `rollback` | Use `v{rollback_version}` instead of releasing a new skill version |

Plugin bumps are inferred automatically from the largest skill bump:
`major` > `minor` > `patch` > no bump. For example, a patch skill bump and a major
skill bump produce a major bump for all three plugins. A rollback counts as a
patch bump so the rolled-back skill content is shipped in a new plugin release.
If every skill strategy is omitted, no skills or plugins are released.

GitHub Releases are the source of truth for skill versions. `SKILL.md` does not
contain a version field. A repository with no prior release starts at `v0.1.0`;
later releases apply the selected semantic-version bump to the latest release.
The release fails if no packaged skill content has changed since that release.

## Syncing

When syncing content between the skills and the plugins the following nodes are checked out:
- `SKILL.md`
- `references`
- `scripts`
- `assets`

The content is then placed in the following locations:

- Cursor and Claude: `skills/{name}`
- Codex: `plugins/temporal/skills/{name}`

## Secrets

| Secret             | Description |
|--------------------|-------------|
| `APP_CLIENT_ID`    | GitHub App **client ID** |
| `APP_PRIVATE_KEY`  | GitHub App private key (PEM) |

The app needs **Contents (write)**, **Pull Requests (write)**, and
**Checks (read)** permissions.

## How to add a new skill repo

1. Install the GitHub App on the new skill repo with Contents (write), Pull Requests (write), and Checks (read).
2. In [`.github/workflows/plugin-release.yml`](.github/workflows/plugin-release.yml) add the new inputs, then append the repo to all skill matrices.
3. In [`.github/workflows/bump-plugin.yml`](.github/workflows/bump-plugin.yml) add a named `download-artifact` step into that skill's dest folder.


```yaml
skill-temporal-example_package_strategy: *skill_package_strategy
skill-temporal-example_rollback_version: *rollback_version
...
skill_repo: [..., skill-temporal-example]
```
