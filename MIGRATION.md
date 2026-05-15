# Migration Guide: From pypi-template to pyproject.toml + hatchling

This guide helps you migrate from `pypi-template` to the modern Python project standard using `pyproject.toml` with `hatchling` build backend.

## Why Migrate?

- **Modern Standard**: `pyproject.toml` is the official Python packaging standard (PEP 517, 518, 621)
- **Simpler Setup**: No need for `setup.py`, `MANIFEST.in`, or multiple requirement files
- **Better Tooling**: Works with `uv`, the fast Python package installer
- **Active Maintenance**: The `c3:python-project` skill provides ongoing support

## Quick Migration Steps

### 1. Create a new `pyproject.toml`

Replace your `.pypi-template` file and `setup.py` with a single `pyproject.toml`:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "your-package-name"
version = "0.1.0"
description = "Your package description"
readme = "README.md"
license = "MIT"
requires-python = ">=3.9"
authors = [
  { name = "Your Name", email = "your@email.com" }
]
dependencies = [
  # your dependencies here
]

[project.optional-dependencies]
dev = ["pytest", "ruff"]

[project.scripts]
your-cli = "your_package.__main__:main"
```

### 2. Consolidate Requirements

Move all dependencies from:
- `requirements.txt` → `[project.dependencies]`
- `requirements.docs.txt` → `[project.optional-dependencies.docs]`
- `requirements.test.txt` → `[project.optional-dependencies.test]`

### 3. Update Makefile

Replace complex virtual environment management with `uv`:

```makefile
run:
	uv run python -m your_package

test:
	uv run pytest -v

install:
	uv sync
```

### 4. Remove Legacy Files

Delete these files (no longer needed):
- `setup.py`
- `MANIFEST.in`
- `requirements.txt`, `requirements.docs.txt`, `requirements.test.txt`
- `tox.ini` (use `uv run pytest` directly or configure in `pyproject.toml`)
- `.pypi-template`

### 5. Update CI/CD

Update GitHub Actions to use `uv`:

```yaml
- uses: astral-sh/setup-uv@v4
- run: uv sync
- run: uv run pytest
```

## File Mapping

| Old (pypi-template) | New (pyproject.toml) |
|---------------------|----------------------|
| `.pypi-template` | `pyproject.toml` |
| `setup.py` | `pyproject.toml` |
| `requirements.txt` | `[project.dependencies]` |
| `requirements.test.txt` | `[project.optional-dependencies.test]` |
| `requirements.docs.txt` | `[project.optional-dependencies.docs]` |
| `MANIFEST.in` | Not needed (hatchling auto-includes) |
| `tox.ini` | `pyproject.toml [tool.pytest]` or use `uv run` |

## Getting Help

Use the `c3:python-project` skill for:
- Creating new projects: `/c3:python-project init my-app`
- Migrating existing projects: `/c3:python-project migrate`

## Timeline

- **2026-04-29**: Deprecation announced
- **2026-XX-XX**: End of support (no updates, no bug fixes)
- **Archive**: Project will be moved to `incubator/archive`

---

*This migration guide was created as part of the pypi-template deprecation process.*