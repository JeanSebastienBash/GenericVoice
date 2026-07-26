# Contributing — Generic Voice

Generic Voice **v1.1** is **feature-complete**. There is no public feature roadmap.

| Channel | Use for |
|---------|---------|
| GitHub Issues | Concrete bugs worth a case-by-case fix |
| Pull requests | Small, focused fixes that keep the existing scope |
| Email `dreamproject-ai@proton.me` | Security reports (preferred) and general questions |

Public documentation is **English only** (`README.md`, `SECURITY.md`, this file,
`doc/`). Keep changes factual. Do not add marketing sections, pricing, or
parallel long manuals.

## Before you open a pull request

- Run `python3 tests/run_all_tests.py` (Python 3.10+ recommended).
- Do not commit secrets, tokens, `.env`, `venv/`, `output/*.wav`, extracted
  `.onnx` models (except the documented Core ZIP archives), or maintainer-only
  paths such as `lib/dev/` and `.cursor/`.
- Interactive menu synthesis must keep using argv lists (never `shell=True`).
- Describe how you verified the change.

Response time is best-effort (solo maintainer).
