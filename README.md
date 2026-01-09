# Codex Snake (Android)

Android-only Snake built with Kivy.

## Quick Start

Run the bootstrap script once from a fresh clone:

```bash
chmod +x scripts/bootstrap_android.sh
./scripts/bootstrap_android.sh
```

## Build APK (Buildozer)

```bash
buildozer android debug
buildozer android deploy run
```

The Buildozer config lives at `buildozer.spec`.

## Run locally (desktop)

```bash
python3 src/main.py
```

## Architecture

See `docs/architecture.md`.
