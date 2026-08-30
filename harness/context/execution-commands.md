# Execution Commands

The canonical commands. Agents run these rather than inventing variants, so
output is comparable across runs and matches CI.

## Harness gates

```bash
python harness/scripts/branch_gate.py --slug <slug> --rebase   # G0
python harness/scripts/health_check.py                          # structural
python harness/scripts/final_checklist.py --slug <slug>         # G5
```

## Backend

```bash
cd backend
uv venv && source .venv/Scripts/activate      # Windows Git Bash
uv pip install -r requirements.txt            # core, ML-free, deployable
uv pip install -r requirements-local.txt      # + offline embeddings (torch)

uvicorn app.main:app --reload                 # http://localhost:8000
pytest -q                                     # tests
ruff check .                                  # lint
python -m app.rag.ingest                      # rebuild the vector index
```

## Frontend

```bash
cd frontend
npm install
npm run dev                                   # http://localhost:5173
npm test -- --run                             # tests
npm run lint
npx tsc --noEmit                              # typecheck
npm run build
```

## Git

```bash
git checkout -b feature/<slug>
git push -u origin feature/<slug>
gh pr create --title "<type>: <desc>" --body-file harness/tasks/active/<slug>/pull-request.md
```

`gh` is authenticated (`shefali289`). Pass `--base` explicitly when the branch
sits on another feature branch rather than `main`. If a token is ever revoked,
push the branch and use the compare URL instead:
`https://github.com/shefali289/portfolio_ai/compare/main...feature/<slug>`

## Notes

- Windows + Git Bash: venv activation is `.venv/Scripts/activate`.
- CI runs Python 3.12; local is 3.14. Verify wheels resolve before pinning.
- Re-ingest whenever `content/*.json` or `EMBEDDING_PROVIDER` changes — Gemini
  and MiniLM vectors have different dimensions and are not interchangeable.
