#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
assets_dir="${root_dir}/src/assets"

menu_mod="${assets_dir}/main_menu.xm"
game_mod="${assets_dir}/gameplay.it"

menu_wav="${assets_dir}/main_menu.wav"
game_wav="${assets_dir}/gameplay.wav"

if ! command -v openmpt123 >/dev/null 2>&1; then
  echo "openmpt123 not found. Install libopenmpt (e.g., brew install libopenmpt)."
  exit 1
fi

if [ ! -f "$menu_mod" ] || [ ! -f "$game_mod" ]; then
  echo "Missing tracker files in ${assets_dir}."
  exit 1
fi

mkdir -p "$assets_dir"

openmpt123 -q -o "$menu_wav" "$menu_mod"
openmpt123 -q -o "$game_wav" "$game_mod"

echo "Generated:"
echo "  $menu_wav"
echo "  $game_wav"
