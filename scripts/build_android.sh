#!/usr/bin/env bash
set -euo pipefail

root_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"${root_dir}/tools/convert_tracker_to_wav.sh"

cd "$root_dir"
pyenv exec python -m buildozer android debug
