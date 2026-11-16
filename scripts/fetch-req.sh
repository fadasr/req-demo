#!/usr/bin/env bash
# Fetch the pinned req release this demo was verified against.
#
#   scripts/fetch-req.sh
#   python3 tools/explorer/build.py --req build/req-release/req --out docs/explorer.html
#
# The SHA-256 is the release asset's, pinned here; the tarball is verified before use.
set -euo pipefail

ROOT=$(cd "$(dirname "$0")/.." && pwd)
REV=3294a46
DEST="$ROOT/build/req-release"
mkdir -p "$DEST"

case "$(uname -sm)" in
  'Darwin arm64')
    TARGET=aarch64-apple-darwin
    SHA=19983e597e06c00631efa02e910fd8a26fe34d9592f1db9b2b57c1b25ee6f5c3
    ;;
  *)
    echo "fetch-req: this script pins the macOS arm64 release; install req from source for $(uname -sm)" >&2
    exit 1
    ;;
esac

if [ -x "$DEST/req" ] && "$DEST/req" --version 2>/dev/null | grep -q "built from *$REV"; then
  echo "req $REV already in build/req-release"
  exit 0
fi

asset="req-$REV-$TARGET.tar.gz"
curl -fsSL --retry 3 -o "$DEST/$asset" \
  "https://github.com/autox-my/req/releases/download/rev-$REV/$asset"
actual=$(shasum -a 256 "$DEST/$asset" | awk '{print $1}')
if [ "$actual" != "$SHA" ]; then
  echo "fetch-req: SHA-256 mismatch for $asset" >&2
  exit 1
fi
tar -xzf "$DEST/$asset" -C "$DEST"
rm -f "$DEST/$asset"
"$DEST/req" --version
