# Gotchas

Things that cost time. Symptom -> cause -> fix.

> Append whenever something surprising happens. Empty sections are fine.

## Environment

- **Python here is 3.14.7** - newer than most wheels target. Verify a package
  resolves (`uv pip compile --python-version 3.14`) before pinning it. A pin
  recalled from memory produced a version that does not exist.
- **No Ollama, no Docker installed.** The GitHub integration must use the
  public REST API, which needs no auth for public repos.
- **`gh` 2.98.0 is installed** at `C:\Program Files\GitHub CLI\gh.exe`, but a
  new shell may be needed for it to be on `PATH`. If `gh auth status` says not
  logged in, `/complete` cannot open a PR — run `gh auth login` once. Remote
  `origin` is `github.com/shefali289/portfolio_ai`.
- **OneDrive locks directories during `git checkout`/`stash`.** Switching
  branches with untracked dirs present can fail with "Permission denied" and
  leave work stashed. Commit before switching branches; if a pop half-fails, the
  work is still in `git stash list`.
- **Windows + Git Bash.** venv activation is `.venv/Scripts/activate`, not
  `bin/activate`. Avoid `-o /dev/null` with `uv` - it fails to persist on Windows.
- **Long chained heredocs in one Bash call are fragile here.** A single
  mismatched terminator silently swallows the rest and the whole command fails.
  Write files one at a time.
- **Bare `uv venv` selected uv-managed Python 3.11 here.** Use
  `uv venv --python 3.14`; otherwise the pinned numpy build does not resolve.
- **`npm create vite` cancels in a non-interactive shell.** Hand-write the small
  scaffold or run the wizard interactively.
- **Package “latest” can violate peer ranges.** TypeScript 7 was incompatible
  with `typescript-eslint@8`; check peer dependencies before pinning a major.
- **ruff B008 flags FastAPI `Depends()` defaults.** Use an `Annotated` dependency
  alias instead of suppressing the rule.
- **PowerShell may block `npm.ps1`/`npx.ps1`.** Use `npm.cmd` and `npx.cmd` so
  Node scripts run without changing machine execution policy.
- **Headless Edge enforces a minimum normal-window width on Windows.** A requested
  375px bitmap may crop a ~492px CSS viewport; use DevTools device metrics and
  verify `innerWidth`, `clientWidth`, and `scrollWidth` before judging layout.

## Deployment

- **Vercel Python bundle limit is 500 MB.** `torch` + `sentence-transformers` is
  ~1 GB installed. Local embeddings cannot be deployed - use Gemini embeddings in
  production and keep `requirements.txt` free of ML dependencies.
- **Index vectors are provider-specific.** Gemini and MiniLM have different
  dimensions. Switching `EMBEDDING_PROVIDER` requires a re-ingest; the index
  stores its provider + dim and must refuse to load a mismatch.

## CI

- **CI gate parsing must match the canonical task table.** The workflow expected
  a nonexistent `## Gate Log` heading while every task used `# 5 · Gates`; parse
  the G1–G5 table rows and accept honestly recorded `PARTIAL`/`SKIPPED` results.
- **CI runs Python 3.12, local is 3.14.** Pin nothing that only resolves on one.
- **App jobs skip until built.** `backend` keys off `backend/app/main.py`,
  `frontend` off `frontend/package.json`. A skipped job reports `SKIPPED`, never
  passed — never relax that to make a pipeline green.
- **The branch gate blocks a PR whose slug has no task directory.** Run
  `/plan <slug>` before opening the PR.
- **Tree scans must exclude dependency and cache directories.** Harness health
  walked into `backend/.venv`; skip generated trees before reading Markdown.

## AI behaviour

_(none yet - expect entries once RAG is running)_
