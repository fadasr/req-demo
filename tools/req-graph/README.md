# tools/req-graph/

Copied from [`autox-my/req`](https://github.com/autox-my/req) at `main` after PR #89, so the demo
can regenerate its graphs without a local checkout of the tool:

- `trace_to_archify.py` — `req.trace/1` → archify architecture pages (ADR 0046/0050).
- `arch_overlay.py` — architecture diagram + `req.satisfy/1` + `req.trace/1` → component overlay
  and coverage matrix (ADR 0052/0053).

They are pinned to archify `7e45f36` (the version `req`'s `examples/graph/README.md` names).
`scripts/fetch-archify.sh` downloads that version into `build/archify/`.
