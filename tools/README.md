# tools/

`needs_import.py` is copied from [`autox-my/req`](https://github.com/autox-my/req) at the commits
that added `--links` and `--tests` (PR #86, branch `feat/needs-import-links`, built from `dd78c81`
plus the change). It is a starting point to copy and adjust, not a `req` subcommand (ADR 0027);
keeping a copy here is what makes the demo reproducible.

To refresh it after the PR lands:

```bash
curl -fsSL https://raw.githubusercontent.com/autox-my/req/main/tools/needs_import.py \
  -o tools/needs_import.py
python3 tools/needs_import.py --self-check
```

The only local difference is nothing: `scripts/import.sh` passes `--links` and `--areas` on the
command line.
