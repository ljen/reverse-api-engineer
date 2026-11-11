# Release Process

This project uses a single source of truth for versioning: `pyproject.toml`. The current declared version is `0.9.0`. Releases are manual; this checkout has no tracked CI publishing workflow. Publishing this fork to the existing PyPI project requires maintainer credentials and is separate from pushing documentation changes.

## How it works

- The version is defined **only** in `pyproject.toml` 
- `src/reverse_api/__init__.py` reads the version dynamically using `importlib.metadata`
- This means you only need to update the version in **one place**

## To create a new release

1. **Update version in `pyproject.toml`**:
   ```toml
   version = "x.y.z"
   ```

2. **Update CHANGELOG.md** with release notes

3. **Validate and build** using the checks in [CONTRIBUTING.md](CONTRIBUTING.md), then:
   ```bash
   uv lock
   uv build
   ```
   For an intentional clean rebuild, `./scripts/clean_build.sh` first deletes `dist/`, `build/`, egg metadata, and Python caches recursively, including caches in `.venv`. Review those targets before using it. Inspect the wheel and source distribution before publishing, especially for local files that are not meant to ship.

4. **Commit and tag**:
   ```bash
   git add pyproject.toml uv.lock CHANGELOG.md
   git commit -m "release: vx.y.z - description"
   git tag vx.y.z -m "Release vx.y.z: description"
   ```

5. **Push the intended release branch and tag** to its configured remote (the commands below assume `origin` and `main`; check `git remote -v` and `git branch -vv` first):
   ```bash
   git push origin main
   git push origin vx.y.z
   ```

6. **Publish to PyPI**, only with release authorization and credentials for `reverse-api-engineer`:
   ```bash
   # Supply UV_PUBLISH_TOKEN through your environment; never commit it.
   uv publish dist/reverse_api_engineer-x.y.z*
   ```

## Important Notes

- **Never manually edit** `src/reverse_api/__init__.py` to change the version
- The version is automatically read from the installed package metadata
- Without installed distribution metadata, the version falls back to `0.0.0.dev`
- After installation, it shows the correct version from `pyproject.toml`
