# Codex Snake (Android)

Android-only Snake built with Kivy.

## Quick Start

Run the bootstrap script once from a fresh clone (it pins `cython<3` and prefers
Python 3.10 when available to avoid `pyjnius` build errors):

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

If you see `pyjnius` errors about `long`, ensure `buildozer.spec` points to
Python 3.10 via `p4a.python_path`.

If Buildozer still uses Python 3.12, run it via the pyenv interpreter:

```bash
rm -rf .buildozer
PYTHON="$(pyenv which python)" "$PYTHON" -m buildozer android debug
```

## Run locally (desktop)

```bash
python3 src/main.py
```

## Tests

```bash
pytest
```

## Architecture

See `docs/architecture.md`.
