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

PYTHON_BIN="python3"
if command -v pyenv >/dev/null 2>&1; then
  if pyenv versions --bare | grep -q "^3.10.14$"; then
    export PYENV_VERSION="3.10.14"
    PYTHON_BIN="$(pyenv which python)"
    echo "==> Using pyenv Python ${PYENV_VERSION} for buildozer."
    echo "==> Set p4a.python_path to this interpreter in buildozer.spec."
    export P4A_PYTHON_PATH="$PYTHON_BIN"
  else
    echo "==> pyenv detected, but Python 3.10.14 is not installed."
    echo "    Install with: pyenv install 3.10.14"
  fi
fi

PYTHON_VERSION="$($PYTHON_BIN -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')"
if [[ "$PYTHON_VERSION" == "3.12" ]]; then
  echo "==> Warning: Python 3.12 detected. pyjnius builds can fail with Cython."
  echo "    Use Python 3.10 (pyenv) or set p4a.python_path in buildozer.spec."
fi

echo "==> Installing Python tooling (buildozer, cython<3)..."
"$PYTHON_BIN" -m pip install --user buildozer "cython<3"

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
echo "  rm -rf .buildozer"
echo "  \"$PYTHON_BIN\" -m buildozer android debug"
