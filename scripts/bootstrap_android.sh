#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "==> Codex Snake Android bootstrap"

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required but was not found on PATH."
  exit 1
fi

if ! command -v pip3 >/dev/null 2>&1; then
  echo "pip3 is required but was not found on PATH."
  exit 1
fi

echo "==> Installing Python tooling (buildozer, cython)..."
python3 -m pip install --user buildozer cython

if ! command -v buildozer >/dev/null 2>&1; then
  echo "buildozer not found on PATH."
  echo "Add this to your shell profile and reopen the terminal:"
  echo "  export PATH=\"\$HOME/Library/Python/3.12/bin:\$PATH\""
fi

if [[ -x "$ROOT_DIR/scripts/check_android_deps.sh" ]]; then
  echo "==> Checking Android dependencies..."
  "$ROOT_DIR/scripts/check_android_deps.sh"
fi

if [[ -x "$ROOT_DIR/scripts/setup_android_sdkmanager.sh" ]]; then
  echo "==> Ensuring sdkmanager is available..."
  "$ROOT_DIR/scripts/setup_android_sdkmanager.sh"
fi

echo "==> Bootstrap complete."
echo "Next:"
echo "  buildozer android debug"
