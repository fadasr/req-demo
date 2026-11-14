#!/usr/bin/env bash
# Show req's drift-and-direction signal on a real claim.
#
# Clones this repository into a temporary directory (so the working tree is never touched),
# weakens the over-temperature shutdown from 100 ms to 500 ms, commits it, and asks req what
# moved between the two revisions. The pin still says 0.1 s, which is the point: a pin catches
# drift even when nobody changed it.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
REQ=${REQ:-req}
CLAIM=claims/REQ-0115.yml
TMP=$(mktemp -d "${TMPDIR:-/tmp}/req-drift.XXXXXX")
trap 'rm -rf "$TMP"' EXIT

git clone -q "$ROOT" "$TMP/corpus"
cd "$TMP/corpus"

perl -pi -e 's/within 100ms/within 500ms/' "$CLAIM"
git add "$CLAIM"
git -c user.name=demo -c user.email=demo@example.invalid commit -qm "weaken the over-temperature shutdown"

echo "== before: the statement and its pin"
git show HEAD~1:"$CLAIM" | grep -E '^(statement|  value):'
echo
echo "== req diff --base HEAD~1 (the weakening is a change in meaning, not an edit)"
"$REQ" diff --base HEAD~1
echo
echo "== the pin the commit did not update (the gate refuses)"
"$REQ" gate 2>&1 | sed -n '/pins_hold/,+2p' || true
