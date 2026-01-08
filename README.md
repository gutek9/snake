# Terminal Snake

Play Snake in your terminal using Python and curses.

## Run

- `python -m snake`
- Or install locally and run `terminal-snake`

## Tests

- `pytest`

## Android (Kivy)

This repo includes a Kivy-based front end for Android.

### Run locally (desktop)

- `python src/main.py`

### Build APK (Buildozer)

Before the first build, check dependencies:

- `scripts/check_android_deps.sh`
- `scripts/setup_android_sdkmanager.sh` (only if sdkmanager is missing)
- `tools/convert_tracker_to_wav.sh` (generate `assets/*.wav` from tracker files)

1) Install Buildozer and Android SDK/NDK
2) `buildozer android debug`
3) `buildozer android deploy run`

The Buildozer config lives at `buildozer.spec`.

## Architecture

- See `docs/architecture.md`
