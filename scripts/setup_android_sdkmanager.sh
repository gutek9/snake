#!/usr/bin/env bash
set -euo pipefail

spec_path="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/buildozer.spec"

sdk_path=""
if [ -f "$spec_path" ]; then
  sdk_path=$(awk -F'=' '/^android\.sdk_path/ {gsub(/^[ \t]+|[ \t]+$/, "", $2); print $2}' "$spec_path")
fi

if [ -z "$sdk_path" ]; then
  sdk_path="$HOME/.buildozer/android/platform/android-sdk"
fi

cmdline="$sdk_path/cmdline-tools/latest/bin/sdkmanager"
legacy="$sdk_path/tools/bin/sdkmanager"

if [ ! -f "$cmdline" ]; then
  echo "cmdline-tools sdkmanager not found at: $cmdline"
  echo "Install the Android SDK command line tools first."
  exit 1
fi

if [ -f "$legacy" ]; then
  echo "Legacy sdkmanager already present at: $legacy"
  exit 0
fi

mkdir -p "$sdk_path/tools/bin"
ln -s "$cmdline" "$legacy"

echo "Linked sdkmanager to legacy path: $legacy"
