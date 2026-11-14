#!/usr/bin/env bash
# Draft req claims from the pinned export.
#
#   scripts/import.sh              # dry run: the whole report, nothing written
#   scripts/import.sh --write      # write the drafts
#
# The types are the requirement types this corpus has. `need` is included because the ADAS
# stakeholder needs are the top of the link chain; arch/component/impl/test are not
# requirements, and the importer counts them as not selected. `--links` carries the typed edges
# between drafts; `--areas` files each claim under its source docname.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PIN=3c602bfedf710d2304d22a93049d7233bba93285
ORIGIN="https://github.com/useblocks/sphinx-needs-demo@$PIN"
DATE=${DATE:-2026-11-14}

if [ ! -f "$ROOT/build/needs.json" ]; then
  echo "import: build/needs.json is missing; run scripts/build-upstream.sh first" >&2
  exit 1
fi

if compgen -G "$ROOT/claims/*.yml" >/dev/null; then
  echo "import: claims/ already holds claims; the importer refuses to draft over a corpus." >&2
  echo "        remove claims/*.yml deliberately (and edit .req/areas) before a fresh import." >&2
  exit 1
fi

types=(req sysreq swreq fsr safety_goal need)
type_args=()
for type in "${types[@]}"; do
  type_args+=(--type "$type")
done

# The Coffee Machine report proves four claims; the ADAS qualification report proves nine more
# and fails three of them, which is the point: the gate reports a failing test, not UNVERIFIABLE.
test_args=()
if [ -f "$ROOT/data/coffee_machine_junit.xml" ] && [ -f "$ROOT/data/adas_junit.xml" ]; then
  test_args=(--tests data/coffee_machine_junit.xml --tests data/adas_junit.xml
             --test-type test --test-link specs --test-link links)
elif [ -f "$ROOT/data/coffee_machine_junit.xml" ]; then
  test_args=(--tests data/coffee_machine_junit.xml --test-type test --test-link specs)
fi

cd "$ROOT"
if [ ${#test_args[@]} -gt 0 ]; then
  python3 tools/needs_import.py \
    --from build/needs.json \
    --origin "$ORIGIN" \
    --date "$DATE" \
    "${type_args[@]}" \
    --links --areas --area-depth 2 \
    "${test_args[@]}" \
    "$@"
else
  python3 tools/needs_import.py \
    --from build/needs.json \
    --origin "$ORIGIN" \
    --date "$DATE" \
    "${type_args[@]}" \
    --links --areas --area-depth 2 \
    "$@"
fi
