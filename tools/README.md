# tools/

`needs_import.py` is copied from [`autox-my/req`](https://github.com/autox-my/req) at the branch
that adds `--links` and `--tests` (PR #86, based on `main` at `b250c3d`; the copy was verified
with `cc35d81`, rules_v 9). It is a starting point to copy and adjust, not a `req` subcommand
(ADR 0027); keeping a copy here is what makes the demo reproducible.

To refresh it after the PR lands:

```bash
curl -fsSL https://raw.githubusercontent.com/autox-my/req/main/tools/needs_import.py \
  -o tools/needs_import.py
python3 tools/needs_import.py --self-check
```

The only local difference is nothing: `scripts/import.sh` passes `--links` and `--areas` on the
command line.
