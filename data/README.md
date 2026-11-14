# data/

- `coffee_machine_junit.xml` — the passing coffee-machine unit tests (4 claims).
- `adas_junit.xml` — the ADAS SYS.5 qualification results: three failures and one skipped case
  (9 claims). The release gate reports this as FAIL, which is the point of committing it.

Both are copied from the pinned upstream checkout at `docs/testsuites/` (commit `3c602bf`, MIT;
see `upstream/LICENSE`). They are committed here so the demo's test links are reproducible
without a built upstream checkout: `scripts/import.sh` points `--tests` at them, and the claims'
`tests:` ids are the `classname::name` strings they carry.
