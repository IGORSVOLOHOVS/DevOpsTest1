# dev-ops-test1 - Software Requirements Specification

Reverse-engineered from the code at commit `f87b08f` on 2026-11-18. Every
requirement describes behaviour that exists in the files named in its source.
Statements marked "inference" are conclusions from the cited evidence, not
stated in the repository.

Short file names in sources: `gate.ps1`, `log.ps1`,
`session-start-stop.ps1` are in `.claude/hooks/`; `commit-msg`,
`commit-msg.ps1`, `pre-push`, `pre-push.ps1` are in `.claude/hooks/git/`;
`*.yaml` files are in `.gitea/workflows/`; `pull_request_template.md` is in
`.gitea/`.

<!-- jira-sync:start -->
Jira: KAN-103

## Tasks

This list is one ticket in Jira project KAN, [KAN-103](https://igorsvolohovs.atlassian.net/browse/KAN-103). Each line is a checkbox there: tick it in Jira and the sync ticks it here; add a checkbox there and it is appended here. Done items are the features described in section 3; open items are what the project declares but the code does not do yet.

- [x] Site (section 3.1) <!-- spec-site -->
- [x] Container image (section 3.2) <!-- spec-container-image -->
- [x] recipe.ps1 (section 3.3) <!-- spec-recipe-ps1 -->
- [x] Claude Code hooks (section 3.4) <!-- spec-claude-code-hooks -->
- [x] Git hooks (section 3.5) <!-- spec-git-hooks -->
- [x] Workflows (section 3.6) <!-- spec-workflows -->
- [ ] Articles for `/blog`: (declared, not implemented) <!-- spec-articles-for-blog -->
- [ ] A pinned pytest: (declared, not implemented) <!-- spec-a-pinned-pytest -->
- [ ] Wiki regeneration: (declared, not implemented) <!-- spec-wiki-regeneration -->
- [ ] Manual testing: (declared, not implemented) <!-- spec-manual-testing -->
- [ ] Installer: (declared, not implemented) <!-- spec-installer -->
- [ ] `$RunArgs` is declared (`recipe.ps1:5-6`) and used by no verb. (declared, not implemented) <!-- spec-runargs-is-declared-recipe-ps1-5-6-and-used-by-no- -->
- [ ] Compliance with "revision 4.0.0" of the lab requirements, except R-02, R-09, (declared, not implemented) <!-- spec-compliance-with-revision-4-0-0-of-the-lab-requirem -->
- [ ] Branch protection stages 1 and 2 (`CLAUDE.md`, last section): (declared, not implemented) <!-- spec-branch-protection-stages-1-and-2-claude-md-last-se -->

<!-- jira-sync:end -->

## 1. Purpose and scope

The repository holds a DevOps exercise (`README.md:3-5`) and the tooling that
governs how the repository itself is changed and released.

In scope:

- the Flask site `site/app.py` and its container image (`Dockerfile`);
- the command interface `recipe.ps1`;
- the Claude Code hooks and skill under `.claude/`;
- the git hooks under `.claude/hooks/git/`;
- the Gitea Actions workflows and templates under `.gitea/`.

Out of scope (absent from the repository): page content beyond three fixed
strings, templates, storage, authentication, a deployment target, an
installer, a wiki generator, manual test definitions.

## 2. Context

| Actor / system | Role | Source |
|---|---|---|
| HTTP client | Requests `/`, `/about`, `/blog` | `site/app.py:5-15` |
| Developer with Claude Code | Runs sessions whose tool calls pass through the hooks | `.claude/settings.json:7-19` |
| Owner (login listed in `$Reviewers`) | Merges into `release`, may write the override | `recipe.ps1:22-23`, `CLAUDE.md` |
| Tester | Records manual test statuses when a manual list exists | `release-gate.yaml:204-219` |
| `lab-bot` | Git identity of the release workflow | `release.yaml:40` |
| Gitea server and API v1 | Hosts pull requests, statuses, releases, generic packages, wiki | `propose.yaml:17`, `release.yaml:290` |
| Gitea Actions runner, label `windows` | Executes the workflows with Windows PowerShell | every workflow, `runs-on: windows`, `shell: powershell` |
| Docker | Builds and runs the image | `README.md:17-22` |

Runtime environment:

- Site: Linux image `python:3.12.2-bookworm` (`Dockerfile:1`), gunicorn as the
  WSGI server (`Dockerfile:11`).
- Tooling: Windows; `powershell.exe` runs every hook (`.claude/settings.json:8-18`,
  `commit-msg:3`, `pre-push:7`); Git for Windows' `sh` runs the git hook
  wrappers (`commit-msg:2`); Python runs pytest and ruff (`recipe.ps1:46-52`).
- The PR template asks that PowerShell parses in 5.1 (`pull_request_template.md:16`).

## 3. Functional requirements

### 3.1 Site

| ID | Requirement | Source | Verification |
|---|---|---|---|
| FR-1 | The system shall answer a request to `/` with the body `MAIN PAGE`. | `site/app.py:5-7` | no test |
| FR-2 | The system shall answer a request to `/about` with the body `THIS IS THE ABOUT PAGE`. | `site/app.py:9-11` | no test |
| FR-3 | The system shall answer a request to `/blog` with the body `HERE WILL BE ARTICLES`. | `site/app.py:13-15` | no test |

### 3.2 Container image

| ID | Requirement | Source | Verification |
|---|---|---|---|
| FR-4 | The image shall be built on `python:3.12.2-bookworm` and contain `site/` at `/site`. | `Dockerfile:1-3` | no test |
| FR-5 | The image build shall install `flask` and `gunicorn` with pip, without version constraints. | `Dockerfile:5` | no test |
| FR-6 | The container shall start gunicorn in `/site` with 5 workers, bound to `0.0.0.0`, serving `app:app`, and declare port 8000. | `Dockerfile:7-11` | no test |

### 3.3 recipe.ps1

| ID | Requirement | Source | Verification |
|---|---|---|---|
| FR-7 | The system shall accept exactly one verb from `build install uninstall clean run publish info test` and reject any other. | `recipe.ps1:1-4` | no test |
| FR-8 | The system shall export each `KEY=VALUE` line of `.claude/.env` as an environment variable, quotes trimmed, unless the variable is already set. | `recipe.ps1:30-38` | no test |
| FR-9 | `test` shall set `core.hooksPath` to `.claude/hooks/git` and exit 1 if git fails. | `recipe.ps1:42-43` | no test |
| FR-10 | `test` shall run `python -m pytest .claude` and treat exit codes 0 and 5 as a pass. | `recipe.ps1:45-48` | manual: collection returns exit 5 (2026-11-18) |
| FR-11 | `test` shall run `ruff check` and then `ruff format` (in place) over `.claude`, exiting 1 on a failure and 0 when all steps pass. | `recipe.ps1:49-54` | no test (called by `propose.yaml:146`; no run observed) |
| FR-12 | `info` shall print `Name`, `Code`, `Version`, `Summary` and exit 0. | `recipe.ps1:56-62` | manual run 2026-11-18 |
| FR-13 | `clean` shall delete every `__pycache__`, `.pytest_cache` and `.ruff_cache` directory under the repository root. | `recipe.ps1:63-68` | no test |
| FR-14 | `build`, `install`, `uninstall`, `run`, `publish` shall print `nothing to <verb>` and exit 0. | `recipe.ps1:69-73` | manual run of `build` 2026-11-18 |

### 3.4 Claude Code hooks

| ID | Requirement | Source | Verification |
|---|---|---|---|
| FR-15 | The system shall register hooks for SessionStart, UserPromptSubmit, PreToolUse (tools `Bash` and `PowerShell`), PostToolUse, Notification, Stop, SubagentStop, PreCompact and SessionEnd. | `.claude/settings.json:7-19` | no test |
| FR-16 | Each logged event shall append one JSON line (`ts`, `event`, `session`, `tool`, and `detail` = first 200 characters of `prompt`, `message`, `reason`, `source` or `file_path`) to `.claude/logs/ai.jsonl`. | `log.ps1:3-24` | no test |
| FR-17 | At SessionStart the system shall move an `ai.jsonl` larger than 10 MB to `ai.jsonl.<yyyyMMddHHmmss>.bak`. | `session-start-stop.ps1:27-30` | no test |
| FR-18 | At SessionStart the system shall set `core.hooksPath`, write an error line to stderr when `recipe.ps1` is missing, log `branch=`, `issue=`, `hooks=`, and return additional context naming the branch and the issue number parsed from it. | `session-start-stop.ps1:31-47` | no test |
| FR-19 | The system shall log Stop as `turn finished` and SessionEnd with its reason. | `session-start-stop.ps1:49-54` | no test |
| FR-20 | The gate shall deny a PreToolUse call whose payload has no readable `tool_name`. | `gate.ps1:2-4`, `gate.ps1:34-36` | no test |
| FR-21 | The gate shall judge each segment of a command separately, after removing quotes, splitting on `\|\|`, `&&`, `;`, `\|`, `&` and newlines, and unwrapping `sudo`, `env`, `VAR=` prefixes and `bash`/`sh`/`cmd`/`powershell`/`pwsh`/`xargs` wrappers. | `gate.ps1:40-57`, `gate.ps1:135-144` | no test |
| FR-22 | The gate shall deny a recursive delete (`rm`, `Remove-Item`, `ri`, `rd`, `rmdir`, `del`, `erase` with `-r`/`-R`/`-Recurse`/`--recursive` or `/s`, and any `rimraf`) unless every path resolves under `$env:TEMP`. | `gate.ps1:83-119`, `gate.ps1:145-154` | no test |
| FR-23 | The gate shall deny `git push` with `--force`, `--mirror`, an `-f` flag bundle or a `+refspec`, and allow `--force-with-lease`. | `gate.ps1:155-163` | no test |
| FR-24 | On branch `test` or `release` the gate shall deny `git reset --hard` (except to `origin/<branch>`, `@{u}`, `@{upstream}`), `git clean -f`/`--force`, `git commit --amend`, `git rebase` and `git filter-branch`. | `gate.ps1:121-129`, `gate.ps1:164-177` | no test |
| FR-25 | The gate shall log every judged call, with `decision: deny` on a denial. | `gate.ps1:6-32`, `gate.ps1:180` | no test |

### 3.5 Git hooks

| ID | Requirement | Source | Verification |
|---|---|---|---|
| FR-26 | `commit-msg` shall refuse a message that starts with a UTF-8 BOM. | `commit-msg.ps1:21-28` | no test |
| FR-27 | `commit-msg` shall pass a subject starting with `Merge ` while `MERGE_HEAD` exists. | `commit-msg.ps1:32-35` | no test |
| FR-28 | `commit-msg` shall require the subject `<type>(<scope>): <text>`, case-sensitive, with types and scopes read from `$CommitTypes` and `$CommitScopes`. | `commit-msg.ps1:7-19`, `commit-msg.ps1:37-47` | no test |
| FR-29 | `commit-msg` shall require a `Signed-off-by: <name> <<address>>` trailer. | `commit-msg.ps1:48-53` | no test |
| FR-30 | `pre-push` shall pass the push to `git lfs pre-push` when `git-lfs` is installed, then to `pre-push.ps1`. | `pre-push:3-7` | no test |
| FR-31 | `pre-push` shall refuse a pushed branch that does not match `<$Code>-<n>/<$BranchTypes>/<slug>`, except `test`, `from-*`, deletions and tags. | `pre-push.ps1:39-41`, `pre-push.ps1:47-53`, `pre-push.ps1:87-93` | no test |
| FR-32 | `pre-push` shall refuse deleting `release`, allow creating it, and refuse updating it unless a first-parent commit not on `origin/test` carries `$OverridePhrase` alone on a line and a `Why: ` line. | `pre-push.ps1:54-86` | no test |
| FR-33 | `pre-push` shall skip judging (exit 0) when `recipe.ps1` is missing or `$BranchTypes` is not a literal list. | `pre-push.ps1:10-13`, `pre-push.ps1:28-31` | no test |

### 3.6 Workflows

| ID | Requirement | Source | Verification |
|---|---|---|---|
| FR-34 | On a pull request into `test`, `propose` shall fail when the head branch (other than `from-*`) breaks the branch grammar. | `propose.yaml:1-5`, `propose.yaml:33-75` | no test |
| FR-35 | `propose` shall fail when a non-merge commit between the merge base and HEAD, not on `release`, has a subject outside the grammar or no `Signed-off-by`. | `propose.yaml:77-142` | no test |
| FR-36 | `propose`, `test` and `release-gate` shall run `recipe.ps1 test` and fail if `git diff --exit-code` then reports changes. | `propose.yaml:144-152`, `test.yaml:54-58`, `release-gate.yaml:49-53` | no test |
| FR-37 | On an opened or reopened pull request, `propose` shall request review from `$Reviewers` other than the poster and post a comment; without `LAB_BOT_TOKEN` it shall warn and pass. | `propose.yaml:154-193` | no test |
| FR-38 | `test` (push to `test`, daily `0 3 * * *`, manual dispatch) shall fail when drive C: has under 5 GB free or `python`, `ruff`, `pytest`, `mypy` do not answer `--version`, and warn under 20 GB. | `test.yaml:2-7`, `test.yaml:32-45` | no test |
| FR-39 | `test` and `release-gate` shall run `recipe.ps1 build`, run the install/uninstall proof only when `$App` is set, and run `recipe.ps1 clean` at the end. | `test.yaml:59-72`, `test.yaml:111-120`, `release-gate.yaml:55-85` | no test |
| FR-40 | `release-gate` shall fail a pull request into `release` whose head branch is not `test`. | `release-gate.yaml:27-31` | no test |
| FR-41 | `manual-gate` shall post `manual/verdict` = success, "no manual tests defined", when `tests/manual/tests.json` is absent or lists no test. | `release-gate.yaml:107-149` | no test |
| FR-42 | With a non-empty manual list, `manual-gate` shall seed `manual/<id>` statuses, poll every 30 s for up to `WAIT_MINUTES`, accept an override comment by a `$Reviewers` login newer than the head commit, reject a verdict whose tests are not green, and store `manual-report.md` as a generic package and an artifact. | `release-gate.yaml:151-446` | no test |
| FR-43 | On a push to `release`, `release` shall read `$Version` and publish nothing when tag `v<$Version>` exists. | `release.yaml:45-60` | no test |
| FR-44 | `release` shall write release notes listing non-merge commits since the last `v*` tag and the issues and pull requests their subjects reference. | `release.yaml:76-124` | no test |
| FR-45 | `release` shall record, for each first-parent commit of the push, merges past a non-green `manual/verdict` or checks and direct pushes, mark such a release as a pre-release, and open or comment an issue when no `Why:` line explains them. | `release.yaml:126-277` | no test |
| FR-46 | `release` shall create release `v<$Version>` and attach the first `dist/*.exe` if present, `manual-report.md` (or a placeholder) and `sbom.md`. | `release.yaml:279-336` | no test |
| FR-47 | `release` shall comment "Shipped in v<version>." on and close the open issues named by merged work branches. | `release.yaml:93-116`, `release.yaml:338-354` | no test |
| FR-48 | `release` shall merge `release` into `test` with `--no-ff` and push it, or open or comment the issue "test is behind release" on failure. | `release.yaml:356-400` | no test |
| FR-49 | `release` shall prepend the notes to `CHANGELOG.md` on `test` only when `$App` or `$Provides` is set. | `release.yaml:402-422` | no test |
| FR-50 | `sweep` (cron `0 4 * * 1`) shall delete remote work branches merged into `test`. | `sweep.yaml:2-4`, `sweep.yaml:23-44` | no test |
| FR-51 | `sweep` shall comment on open pull requests idle 30 days or more and close those idle 60 days or more. | `sweep.yaml:45-80` | no test |

### 3.7 Declared but not implemented

- Articles for `/blog`: the response text announces them (`site/app.py:15`);
  there is no code or data for articles.
- A pinned pytest: commit `8393f05` is titled "pin ruff and pytest"; only ruff
  is pinned (`.claude/ruff.toml:2`), `.claude/pytest.ini:1-2` has no version.
- Wiki regeneration: `test.yaml:85` and `test.yaml:106` call `tools/wiki.py`,
  which is not in the repository; the step runs only when `$App` or
  `$Provides` is set (`test.yaml:74`), and neither is (`recipe.ps1:16-17`).
- Manual testing: `release-gate.yaml:210` tells testers to run
  `tests/manual/serve.py`; neither it nor `tests/manual/tests.json` exists.
- Installer: `release-gate.yaml:63` and `release.yaml:296` look for
  `dist/*.exe`; `recipe.ps1 build` produces nothing (`recipe.ps1:69-73`).
- `$RunArgs` is declared (`recipe.ps1:5-6`) and used by no verb.
- Compliance with "revision 4.0.0" of the lab requirements, except R-02, R-09,
  R-41, R-42 (`README.md:39`): the requirements document is external and the
  claim cannot be checked from the repository.
- Branch protection stages 1 and 2 (`CLAUDE.md`, last section): server
  settings, nothing in the repository implements them.

## 4. Interfaces

### 4.1 HTTP (gunicorn, `site/app.py`)

| Path | Body | Source |
|---|---|---|
| `/` | `MAIN PAGE` | `site/app.py:5-7` |
| `/about` | `THIS IS THE ABOUT PAGE` | `site/app.py:9-11` |
| `/blog` | `HERE WILL BE ARTICLES` | `site/app.py:13-15` |

Inference from Flask defaults (no `methods=` given): the routes accept GET
(Flask adds HEAD and OPTIONS), answer `200` with `text/html; charset=utf-8`,
and other paths answer `404`. Inference from gunicorn defaults: `-b 0.0.0.0`
without a port listens on 8000, matching `EXPOSE 8000` (`Dockerfile:9`).

### 4.2 CLI `recipe.ps1`

| Verb | Effect | Exit | Source |
|---|---|---|---|
| `test` | hooksPath, pytest, ruff check, ruff format | 0 pass, 1 fail | `recipe.ps1:41-55` |
| `info` | four metadata lines | 0 | `recipe.ps1:56-62` |
| `clean` | removes cache directories | 0 | `recipe.ps1:63-68` |
| `build`, `install`, `uninstall`, `run`, `publish` | prints `nothing to <verb>` | 0 | `recipe.ps1:69-73` |

### 4.3 Hooks

| Hook | Trigger | Output | Source |
|---|---|---|---|
| `gate.ps1` | PreToolUse, Bash/PowerShell | JSON `permissionDecision: deny` with a reason, or nothing | `gate.ps1:25-32` |
| `session-start-stop.ps1` | SessionStart, Stop, SessionEnd | SessionStart: JSON `additionalContext` | `session-start-stop.ps1:44-47` |
| `log.ps1` | UserPromptSubmit, PostToolUse, Notification, SubagentStop, PreCompact | log line only | `log.ps1` |
| `commit-msg` | git commit | exit 1 with a message on refusal | `commit-msg.ps1` |
| `pre-push` | git push; stdin `<local ref> <local sha> <remote ref> <remote sha>` | exit 1 on refusal | `pre-push.ps1:1` |

### 4.4 Workflows

| Workflow | Trigger | Jobs (timeout) | Source |
|---|---|---|---|
| `propose` | pull request into `test`: opened, reopened, synchronize | `gate` (60 min) | `propose.yaml:2-15` |
| `test` | push to `test`; cron `0 3 * * *`; manual | `prove` (60 min) | `test.yaml:2-17` |
| `release-gate` | pull request into `release` | `checks` (60 min), `manual-gate` (170 min) | `release-gate.yaml:2-91` |
| `release` | push to `release` | `publish` (60 min) | `release.yaml:2-14` |
| `sweep` | cron `0 4 * * 1` | `sweep` (15 min) | `sweep.yaml:2-14` |

Commit status contexts written: `manual/<id>`, `manual/verdict`
(`release-gate.yaml:185`, `release-gate.yaml:145`); read:
`release-gate / checks (pull_request)` (`release.yaml:194`).

### 4.5 Text formats read by the tooling

| Item | Format | Source |
|---|---|---|
| `recipe.ps1` metadata | one-line literals `$Name = '...'`, `$X = @('a', 'b')`, read by regular expression | `propose.yaml:49-55`, `pre-push.ps1:16-45` |
| Branch name | `^<code>-[1-9][0-9]*/(<types>)/[a-z0-9]+(-[a-z0-9]+)*$` | `pre-push.ps1:41`, `propose.yaml:70` |
| Commit subject | `^(<types>)\((<scopes>)\): .+` | `commit-msg.ps1:40`, `propose.yaml:132` |
| Owner's override | `$OverridePhrase` alone on a line plus `Why: <reason>` | `pre-push.ps1:74-77`, `release-gate.yaml:274-303` |
| `.claude/.env` | `KEY=VALUE` per line | `recipe.ps1:33` |
| `tests/manual/tests.json` | `{"tests": [{"id", "title", "blocking"}]}`; id `^[a-z0-9][a-z0-9_-]{0,60}$`, unique, not `verdict` | `release-gate.yaml:111-134` |

## 5. Data

- The site stores nothing and reads no data (`site/app.py`).
- `.claude/logs/ai.jsonl`: JSON lines, UTF-8 without BOM, fields `ts`,
  `event`, `session`, `tool`, `decision`, `detail` (`log.ps1:4-18`,
  `gate.ps1:8-15`); gitignored (`.gitignore:17`). It holds prompt text
  (`CLAUDE.md`, rule 5).
- `.claude/logs/report-<date>.md`: written by the `lab-ai-env` skill
  (`.claude/skills/lab-ai-env/SKILL.md:48`).
- `.claude/.env`: local keys, gitignored (`.gitignore:24`), absent from every
  commit (`CLAUDE.md`, rule 4).
- On Gitea: release `v<$Version>` with assets `manual-report.md`, `sbom.md`
  and an optional installer (`release.yaml:290-336`); generic packages
  `<name>-manual-reports/<sha>/manual-report.md` and
  `<name>-manual-evidence/<sha>/` (`release-gate.yaml:431-440`); issues titled
  "release changed past the gate without the owner's override" and "test is
  behind release" (`release.yaml:258`, `release.yaml:382`).
- Runner workspace files: `release-body.md`, `issues-to-close.txt`,
  `manual-report.md`, `sbom.md` (`release.yaml:116-332`).

## 6. Non-functional requirements

| ID | Requirement | Source |
|---|---|---|
| NFR-1 | The base image version is fixed at `python:3.12.2-bookworm`; application packages are not (`flask`, `gunicorn` unpinned, no lock file). | `Dockerfile:1`, `Dockerfile:5` |
| NFR-2 | gunicorn runs 5 worker processes. | `Dockerfile:11` |
| NFR-3 | ruff refuses to run unless its version is `0.16.1`. | `.claude/ruff.toml:2` |
| NFR-4 | Job timeouts: 60 min (`propose`, `test`, `release-gate/checks`, `release`), 170 min (`manual-gate`, waiting up to 150 min), 15 min (`sweep`). | workflow `timeout-minutes`, `release-gate.yaml:101` |
| NFR-5 | Jobs that build an installer share concurrency group `installer-<repo>` without cancellation; `release-gate` cancels an older run of the same pull request; `release` runs one at a time per repository. | `test.yaml:18-20`, `release-gate.yaml:7-9`, `release-gate.yaml:20-22`, `release.yaml:15-17` |
| NFR-6 | `manual-gate` polls every 30 s and stops after 10 consecutive failed polls; status reads page through up to 40 pages of 50. | `release-gate.yaml:161`, `release-gate.yaml:323-337` |
| NFR-7 | Log appends retry 20 times on a file-in-use error, waiting 10 x n ms; `detail` is cut at 200 characters; the log rotates above 10 MB. | `log.ps1:10`, `log.ps1:20-24`, `session-start-stop.ps1:28` |
| NFR-8 | An override reason is cut to 100 characters in the status description. | `release-gate.yaml:310` |
| NFR-9 | No key is committed: `.claude/.env`, `.claude/logs/` and `.claude/settings.local.json` are gitignored; workflows take the token from the secret `LAB_BOT_TOKEN`; `test.yaml` and `release.yaml` check out with `persist-credentials: false`. | `.gitignore:17-24`, `test.yaml:30`, `release.yaml:35` |
| NFR-10 | Line endings: LF by default, CRLF with UTF-8 working-tree encoding for `*.ps1`, CRLF for `*.bat`/`*.cmd`, LF for the two sh hook wrappers; `*.pdf`, `*.png`, `*.jpg`, `*.zip`, `*.7z` go to Git LFS. | `.gitattributes:1-13` |
| NFR-11 | Python in Claude Code sessions uses UTF-8 (`PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`); commit messages with a BOM are refused. | `.claude/settings.json:3-4`, `commit-msg.ps1:21-28` |
| NFR-12 | The tooling runs on Windows with Windows PowerShell; workflows need a runner labelled `windows`. | `.claude/settings.json:8-18`, `runs-on: windows` in every workflow |

## 7. Constraints and dependencies

No `requirements.txt`, `pyproject.toml`, `uv.lock` or other lock file is
tracked (`git ls-files`).

| Dependency | Version | Source |
|---|---|---|
| Python (image) | 3.12.2, Debian bookworm | `Dockerfile:1` |
| Flask | unpinned | `Dockerfile:5` |
| gunicorn | unpinned | `Dockerfile:5` |
| ruff | `==0.16.1` | `.claude/ruff.toml:2` |
| pytest | unpinned | `recipe.ps1:46`, `.claude/pytest.ini` |
| mypy | unpinned, runner health check only | `test.yaml:38` |
| uv | optional, used when `uv.lock` exists | `test.yaml:37-41`, `release.yaml:329` |
| Windows PowerShell, git, Git for Windows `sh` | not stated | `.claude/settings.json`, `commit-msg:2` |
| git-lfs | optional | `pre-push:4-6` |
| `curl.exe` | not stated | `release-gate.yaml:439-440`, `release.yaml:298` |
| `actions/checkout` | `v4` | every workflow |
| `actions/upload-artifact` | `v3` | `release-gate.yaml:442` |
| Docker | not stated | `README.md:17` |

Licence: MIT (`LICENSE`).

## 8. Acceptance

1. `.\recipe.ps1 test` exits 0 (`CLAUDE.md`, rule 3); with no tests the pytest
   step returns 5, which passes (`recipe.ps1:48`). Requires `ruff==0.16.1`.
2. `.\recipe.ps1 info` prints the four metadata lines and exits 0 (FR-12).
3. `.\recipe.ps1 build` prints `nothing to build` and exits 0 (FR-14).
4. On Gitea: `propose / gate` green on a pull request into `test`;
   `release-gate / checks` and `manual-gate` green on the pull request from
   `test` into `release` (`CLAUDE.md`).
5. Manual check of FR-1..FR-6: build and run the image with the commands in
   `README.md:19-22`, request `/`, `/about`, `/blog` on port 8000 and compare
   the bodies with section 4.1.
6. No automated test covers any requirement. FR-10, FR-12 and FR-14 were
   checked by hand on 2026-11-18 (see `docs/README.md`, "About this
   document").

## 9. Open questions

- Who the exercise was for (a course, an interview, self-study) and who reads
  the site; `README.md` says only "a DevOps exercise".
- Where, if anywhere, the image is deployed, behind what proxy, with which
  port mapping and TLS; no deployment file exists.
- Which Flask and gunicorn versions the 2024 image used; nothing records them.
- Why 5 gunicorn workers; no load target is stated.
- Whether a Gitea runner serves this repository and whether the workflows have
  run. The lightweight tag `v1.0.0` on `f87b08f` matches what
  `release.yaml:290-293` creates (inference), but the repository does not show
  who created it.
- How the GitHub copy relates to the Gitea repository the workflows target;
  GitHub does not execute `.gitea/workflows` (inference).
- What R-41 and R-42 of the lab requirements require; only R-02 and R-09 are
  described (`CLAUDE.md`), and issues #7-#10 are on the Gitea server.
- Whether `/blog` articles are still planned.
- Whether `mypy` in the runner health check (`test.yaml:38`) is meant for this
  repository, which has no Python code under `.claude`.
