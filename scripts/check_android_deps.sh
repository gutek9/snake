#!/usr/bin/env bash
set -euo pipefail

missing=0

check_cmd() {
  local name="$1"
  local hint="$2"
  if ! command -v "$name" >/dev/null 2>&1; then
    echo "Missing: $name"
    echo "  Hint: $hint"
    missing=1
  fi
}

check_cmd "python3" "Install Python 3.8+ from python.org or via Homebrew."
check_cmd "pip3" "python3 -m ensurepip --upgrade"
check_cmd "git" "Install Xcode Command Line Tools or Homebrew."
check_cmd "java" "brew install openjdk"

if ! python3 -m pip show buildozer >/dev/null 2>&1; then
  echo "Missing: buildozer (pip package)"
  echo "  Hint: python3 -m pip install --user buildozer"
  missing=1
fi

if ! python3 -m pip show cython >/dev/null 2>&1; then
  echo "Missing: cython (pip package)"
  echo "  Hint: python3 -m pip install --user cython"
  missing=1
fi

sdk_path="${HOME}/.buildozer/android/platform/android-sdk"
cmdline="${sdk_path}/cmdline-tools/latest/bin/sdkmanager"
legacy="${sdk_path}/tools/bin/sdkmanager"
if [ ! -f "$cmdline" ] && [ ! -f "$legacy" ]; then
  echo "Missing: Android sdkmanager"
  echo "  Hint: scripts/setup_android_sdkmanager.sh"
  missing=1
fi

if [ "$missing" -eq 0 ]; then
  echo "All required tools found."
  echo "Next: buildozer android debug"
fi

exit "$missing"
