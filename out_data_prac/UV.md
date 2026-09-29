# uv — Quick Reference

## `uv sync`

Does two things:

1. Creates a virtual environment (`.venv/`) — isolated Python for this project only
2. Installs all packages listed in `pyproject.toml`

You don't run `pip install` manually.

After syncing, activate the venv:

```bash
source .venv/bin/activate
```

---

## Add a package (recommended)

```bash
uv add requests
```

That will:

- Install `requests`
- Add it to `pyproject.toml` for you
- Update the lockfile (`uv.lock`)

---

## Remove a package

```bash
uv remove requests
```

---

## Manual edit also works

Add a line in `pyproject.toml`, then run:

```bash
uv sync
```

This installs whatever is listed in the file.
