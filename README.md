# Codex Snake (Android)

Android-only Snake built with Kivy.

## Run

- Build and deploy using `buildozer android debug`

## Android (Kivy)

This repo includes a Kivy-based front end for Android.

### Run locally (desktop)

- `python src/main.py`

### Build APK (Buildozer)

Before the first build, check dependencies:

- `scripts/check_android_deps.sh`
- `scripts/setup_android_sdkmanager.sh` (only if sdkmanager is missing)

1) Install Buildozer and Android SDK/NDK
2) `buildozer android debug`
3) `buildozer android deploy run`

The Buildozer config lives at `buildozer.spec`.

## Architecture

- See `docs/architecture.md`
