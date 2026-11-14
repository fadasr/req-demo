#!/usr/bin/env bash
# Build the pinned sphinx-needs-demo export and copy its needs.json into build/.
#
#   scripts/build-upstream.sh              # the default variant (eu_left)
#   scripts/build-upstream.sh eu_right     # variants/eu_right.json
#
# Needs: git, graphviz (dot), java, uv. The upstream build is the only networked step; after
# it, every req command in this repository runs offline.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
UPSTREAM="$ROOT/upstream"
PIN=3c602bfedf710d2304d22a93049d7233bba93285
REPO=https://github.com/useblocks/sphinx-needs-demo.git
VARIANT=${1:-eu_left}

command -v git >/dev/null || { echo "build-upstream: git is required" >&2; exit 1; }
command -v uv >/dev/null || { echo "build-upstream: uv is required" >&2; exit 1; }
command -v dot >/dev/null || {
  echo "build-upstream: graphviz 'dot' is required by the upstream conf.py (brew install graphviz)" >&2
  exit 1
}

if [ ! -d "$UPSTREAM/.git" ]; then
  git clone -q "$REPO" "$UPSTREAM"
fi
git -C "$UPSTREAM" fetch -q --depth 1 origin "$PIN" 2>/dev/null || true
git -C "$UPSTREAM" checkout -q "$PIN"

variant_args=()
if [ "$VARIANT" != "eu_left" ]; then
  if [ ! -f "$UPSTREAM/docs/variants/$VARIANT.json" ]; then
    echo "build-upstream: no docs/variants/$VARIANT.json upstream" >&2
    exit 1
  fi
  variant_args=(-D "needs_variant_data_file=variants/$VARIANT.json")
fi

uv sync -q --project "$UPSTREAM"
out="$ROOT/build/sphinx-$VARIANT"
mkdir -p "$ROOT/build"
uv run -q --project "$UPSTREAM" sphinx-build -q -b html "${variant_args[@]}" \
  "$UPSTREAM/docs" "$out"

if [ "$VARIANT" = "eu_left" ]; then
  target="$ROOT/build/needs.json"
else
  target="$ROOT/build/needs-$VARIANT.json"
fi
cp "$out/needs.json" "$target"
echo "built $VARIANT from $PIN -> ${target#"$ROOT"/}"
