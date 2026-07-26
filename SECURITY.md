# Security — Generic Voice

Generic Voice is a local text-to-speech integrator (CLI + optional GUI).

## Report a vulnerability

Email **dreamproject-ai@proton.me** with enough detail to reproduce the issue.
Do **not** open a public GitHub issue for unfixed remote-code, secret, or
privilege-escalation flaws.

## Supported line

Only **v1.0.2** is supported. There is no regular hardening roadmap. Fixes are
considered case by case.

## Operator expectations

- Prefer a virtualenv and a non-root user.
- Do **not** run the whole application as root. If system packages are missing,
  install them with your OS package manager, then re-run
  `python3 py/gv.py --auto-fix` as a normal user for Python-side checks.
- `--tts edge` sends synthesis text to a remote Microsoft service. Use Piper or
  eSpeak for offline / private text.
- Review generated audio paths under `output/` before sharing them.
- Keep maintainer-only trees (local `.cursor/`, `lib/dev/`, private Bible) off
  public remotes.

## Project status

Generic Voice **v1.0.2** is **feature-complete**. Maintenance is reactive and
best-effort. See the [README](README.md#project-status) and the
[official project page](https://dreamproject.online/prj/genericvoice).
