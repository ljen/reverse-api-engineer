# Contributing 

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/ljen/reverse-api-engineer.git
   cd reverse-api-engineer
   ```

2. **Install dependencies**
   ```bash
   uv sync --locked
   uv run playwright install chromium
   ```

3. **Run locally**
   ```bash
   uv run reverse-api-engineer
   ```

Python 3.11+ is required; `.python-version` selects 3.13 for uv. The `dev` dependency group includes pytest, pytest-asyncio, pytest-cov, Ruff, and mypy. Optional Copilot support is installed with `uv sync --locked --extra copilot`. Cursor installs its npm bridge dependencies on first use; see the [README](README.md#sdk-selection) for runtime/authentication requirements.

## Validation

Run the tests with an isolated application home so CLI imports and synthetic runs do not read or update your real `~/.reverse-api` history:

```bash
# Run from the repository root after uv sync.
validation_home=$(mktemp -d)
HOME="$validation_home" .venv/bin/python -m pytest
```

The suite uses fixtures and mocks for captures and SDK calls. Some CLI tests invoke `uv run` in a subprocess; they also inherit this temporary home. Do not use live captures or run the example clients merely to validate a documentation change.

Configured static checks (these commands do not auto-fix files):

```bash
uv run ruff check src tests
uv run ruff format --check src tests
uv run mypy src/reverse_api
```

These are available checks, not a claim that the current tree passes all of them. For documentation-only edits, compare commands/defaults with source, check relative links and `git diff --check`, and use isolated CLI help or targeted mocked tests as appropriate. Do not run `scripts/clean_build.sh` for documentation validation: it deletes build outputs and recursively removes Python caches.

## Code Style

- Follow PEP 8 guidelines
- Use type hints where applicable
- Add docstrings to functions and classes

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Test your changes locally
4. Submit a pull request with a clear description

## Reporting Issues

- Use the issue tracker for the fork or upstream repository affected
- Include steps to reproduce
- Provide system information (OS, Python version)
- Include error messages and logs

## Questions?

Feel free to open an issue for any questions or suggestions!
