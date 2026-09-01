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

| Strategy | Skills | Plugins | Effect |
|----------|--------|---------|--------|
| `patch` / `minor` / `major` | yes | yes | 1. Bump version<br>2. Open a release PR and auto merge it<br>3. Create a GitHub Release<br>4. Use this new release |
| `latest` | yes | yes | Use the latest release instead of releasing a new version |
| `rollback` | yes | no | Use `v{rollback_version}` instead of releasing a new version |

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

The app needs **Contents (write)** and **Pull Requests (write)** permissions.

## How to add a new skill repo

1. Install the GitHub App on the new skill repo with Contents (write) and Pull Requests (write).
2. In [`.github/workflows/plugin-release.yml`](.github/workflows/plugin-release.yml) add the new inputs, then append the repo to all skill matrices.
3. In [`.github/workflows/bump-plugin.yml`](.github/workflows/bump-plugin.yml) add a named `download-artifact` step into that skill's dest folder.


```yaml
skill-temporal-example_package_strategy: *skill_package_strategy
skill-temporal-example_rollback_version: *rollback_version
...
skill_repo: [..., skill-temporal-example]
```
