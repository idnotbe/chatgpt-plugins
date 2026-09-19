# idnotbe ChatGPT/Codex plugin marketplace

A metadata-only catalog for **deep-inquiry**, **skill-quality-builder** and
**vibe-check**. Each plugin remains in its own source repository. This hub is
not a plugin and does not contain copies of skill instructions or runtime code.

## Register and install

With a current compatible Codex CLI:

```sh
codex plugin marketplace add idnotbe/chatgpt-plugins
codex plugin marketplace list
```

In the compatible ChatGPT desktop plugin UI, select the **idnotbe Skills**
marketplace (`idnotbe-chatgpt-plugins`) and install the desired plugin. Registering
a catalog through the CLI is not the same as installing a plugin through the UI.
For ChatGPT web/workspace distribution, an authorized administrator imports or
syncs the GitHub marketplace using the available workspace plugin-management
controls. Availability depends on account, workspace policy and host version;
this repository does not automatically install into a remote account or publish
to a universal public plugin directory.

For Claude, use the separate [Claude hub](https://github.com/idnotbe/claude-plugins):

```sh
claude plugin marketplace add idnotbe/claude-plugins
claude plugin install deep-inquiry@idnotbe
claude plugin install skill-quality-builder@idnotbe
claude plugin install vibe-check@idnotbe
```

## Catalog

| Plugin | Purpose | Source |
| --- | --- | --- |
| deep-inquiry | Investigate problems beyond familiar answers while preserving the user objective. | [Repository](https://github.com/idnotbe/deep-inquiry) |
| skill-quality-builder | Create, improve, and audit reusable Agent Skills with explicit validation and evaluation. | [Repository](https://github.com/idnotbe/skill-quality-builder) |
| vibe-check | Assess whether the next action should proceed, be adjusted, or stop. | [Repository](https://github.com/idnotbe/vibe-check) |

## Standalone skills instead of plugins

Use Node.js LTS (CI uses 24), npm and Git. Run from the project receiving the skills:

```sh
npx skills@latest add idnotbe/deep-inquiry --skill deep-inquiry --agent codex claude-code --copy
npx skills@latest add idnotbe/skill-quality-builder --skill skill-quality-builder --agent codex claude-code --copy
npx skills@latest add idnotbe/vibe-check --skill vibe-check --agent codex claude-code --copy
```

Add `--global` for user scope, or select only one agent. `--copy` avoids Windows
symlink privileges; PowerShell may use `npx.cmd` instead of `npx.ps1`. Do not weaken
execution policy. Prefer one installation mode per host/scope to avoid duplicates.
Local skill installation does not modify a ChatGPT web account.

## Shared distribution contract

Each source repo retains `.agents/skills/<name>/` as its single canonical bundle.
Matching `.claude-plugin/plugin.json` and `.codex-plugin/plugin.json` manifests
point to that folder. No root portable manifest, duplicated skills, MCP server,
automatic hook or model API dependency is introduced by these wrappers.

Both hubs preserve the existing default-branch tracking policy: source entries
use bare Git URLs without `ref` or `sha`. They are not reproducible pins. Review
and test changes before merging source releases, bump both source manifest
versions together, and record actual source SHA, CLI versions and installed-file
hashes when verifying a deployment. Use a reviewed fixed checkout and pinned
installer for a reproducible standalone installation. Back up local modifications
before updating and retain a reviewed prior checkout for rollback.

## Verification

Python 3.10+ is needed only for repository checks. No runtime code is installed
from this catalog. Run static checks without network access:

```sh
python -B -m unittest discover -s tests -p test_catalog.py -v
python -B tools/check_catalog.py
```

The explicit integration evaluation requires current official host CLIs, Git,
Node/npm and network access:

```sh
python -B tools/check_catalog.py --smoke --report catalog-report.json
```

Native Windows/Linux CI performs real GitHub-source `npx skills@latest` installs
for both agents, compares every installed file against a recorded source commit,
and checks that all three source repos use identical distribution tooling. It
registers this catalog and uses the **development-only** Codex app-server preview
API to read, install and inspect each plugin and its skill files in an isolated
home/project. These API calls are tests, not a supported production client recipe.
No model turn is started and no LLM credentials are required. The Claude hub uses
the same checker to validate and install the same three external Git plugins.

Inspect the actual CI conclusion and JSON artifact for the exact revision.
Configured tests are not passing tests. GUI installation, ChatGPT web/workspace
import, natural skill triggering and model effectiveness are separate checks,
explicitly recorded as `not_run`, not inferred from installer success.

## Upstream specifications

- [OpenAI plugin and marketplace format](https://developers.openai.com/plugins/build/plugins)
- [ChatGPT plugins](https://learn.chatgpt.com/docs/plugins)
- [App-server development API](https://learn.chatgpt.com/docs/app-server)
- [Skills installer](https://github.com/vercel-labs/skills)

See [LICENSE](LICENSE) for the catalog's license. Each source plugin retains its
own license terms; the hub license does not relicense upstream content.
