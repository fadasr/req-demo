#!/usr/bin/env bash
# Record every `req-satisfies:` declaration under design/ (ADR 0040). This is the human act the
# command names: the files were reviewed, and the record stores each claim's statement verbatim.
# Re-running replaces the same links, so it is safe after a design edit.
#
#   scripts/record-satisfaction.sh
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
REQ=${REQ:-req}
log=$(mktemp "${TMPDIR:-/tmp}/req-record.XXXXXX")
trap 'rm -f "$log"' EXIT
count=0

while IFS= read -r file; do
  rel=${file#"$ROOT/"}
  while IFS= read -r claim; do
    # req prints the resolved corpus root on stderr for every call; keep it out of the report but
    # show it (and the command's error) if the record is refused.
    if ! "$REQ" satisfy --record "$rel" "$claim" >/dev/null 2>"$log"; then
      cat "$log" >&2
      exit 1
    fi
    count=$((count + 1))
  done < <(sed -n 's/.*req-satisfies:[[:space:]]*\([A-Za-z0-9_-][A-Za-z0-9_-]*\).*/\1/p' "$file")
done < <(find "$ROOT/design" -type f | sort)

echo "recorded $count satisfaction link(s)"
