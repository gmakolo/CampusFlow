#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"
if command -v gnome-terminal >/dev/null 2>&1; then
  exec gnome-terminal --working-directory="$PWD" -- python3 main.py
fi
exec python3 main.py
