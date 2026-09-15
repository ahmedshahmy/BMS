#!/usr/bin/env bash
# Preview the BMS newsletter locally:  ./serve.sh [port]
#
# A static server is needed because the site lazy-loads one small script per
# issue. (Every page also works by opening index.html directly, since the
# article text is inlined into those scripts, but a server is closer to how it
# actually gets published.)
set -euo pipefail

PORT="${1:-8099}"
cd "$(dirname "$0")"

if [ ! -f issues/index.js ]; then
  echo "No issues found yet - generating them first..."
  python3 tools/build.py
fi

echo "BMS newsletter -> http://127.0.0.1:${PORT}/index.html"
echo "Press Ctrl+C to stop."
exec python3 -m http.server "$PORT" --bind 127.0.0.1
