#!/usr/bin/env bash
# Download the archify version req's graph tooling pins (7e45f36) into build/archify/.
# The page renderers are committed; this is only needed to regenerate them.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
PIN=7e45f36
DEST="$ROOT/build/archify"

if [ -f "$DEST/archify/bin/archify.mjs" ]; then
  echo "archify $PIN already in build/archify"
  exit 0
fi

mkdir -p "$DEST"
curl -fsSL --retry 3 -o "$ROOT/build/archify.tar.gz" \
  "https://codeload.github.com/tt-a1i/archify/tar.gz/$PIN"
tar -xzf "$ROOT/build/archify.tar.gz" -C "$DEST" --strip-components=1
rm -f "$ROOT/build/archify.tar.gz"
echo "archify $PIN -> build/archify"
