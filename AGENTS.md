# Repository Guidelines

## Project Structure & Module Organization
This repository is currently empty at the root (`/Users/madamek/work/gravitee/workdir/ai-playground`). When adding code, keep a clear top-level layout (for example: `src/` for source, `tests/` for test code, `docs/` for documentation, `scripts/` for tooling). If you introduce assets (images, fixtures, sample data), store them under a dedicated `assets/` or `fixtures/` directory to keep the root tidy.

## Build, Test, and Development Commands
No build or test commands are defined yet. When you add a build system, document the primary developer workflows here with short examples, such as:
- `npm run build` for production builds
- `npm test` or `pytest` for tests
- `make dev` for a local dev server

## Coding Style & Naming Conventions
No style rules are defined yet. Establish a consistent indentation style (e.g., 2 or 4 spaces) and adopt a formatter/linter appropriate to the language (for example: `prettier`, `eslint`, `black`, `ruff`, or `gofmt`). Use clear, descriptive names for modules and files (for example: `user_service.ts`, `order_controller.py`).

## Testing Guidelines
No testing framework is configured yet. Pick a framework that matches the language (for example: `jest`, `pytest`, `go test`) and keep test files grouped under `tests/` or co-located with source. Prefer descriptive test names, such as `test_user_login_success()` or `should_return_404_on_missing_id()`.

## Commit & Pull Request Guidelines
There is no Git history available in this workspace, so commit conventions are not established. Until a project standard exists, use Conventional Commits (for example: `feat: add user creation endpoint`, `fix: handle null payload`). For pull requests, include a clear description, link related issues when available, and note any required setup or migration steps.

## Security & Configuration Tips
Keep secrets out of the repository. Store credentials in environment variables or local config files that are gitignored (for example: `.env`). Document any required configuration in `docs/`.
