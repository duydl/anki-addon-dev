# Anki Add-ons

This repository contains Anki add-ons and development utilities.

## Setting Up the Environment

Anki ships Python wheels to PyPI (current series 25.9.x) built for CPython 3.9+. Use [uv](https://docs.astral.sh/uv/) to manage the virtual environment from the `pyproject.toml`.

1. Install uv (once per machine):

```bash
curl -Ls https://astral.sh/uv/install.sh | sh  # or: pip install uv
```
2. Create the virtual environment and install the dependencies defined in `pyproject.toml` (Anki and AQT):

```bash
uv sync --python 3.11      # use another 3.9+ interpreter if preferred
source .venv/bin/activate  # on Windows: .venv\\Scripts\\activate
```

`uv sync` will resolve and install `anki`/`aqt` along with their Qt runtime into `.venv/`.

3. Run tools via uv when needed:
```bash
uv run python release.py
```

## Running Anki from this repo

Use the helper script to start Anki pointing at a custom base (profile/addons) directory. By default it uses `./_data` inside this repo, which already contains empty `addons21/`, `collection.media`, and a `Test` profile (structure kept with `.gitignore` files):

```bash
./start-anki.sh

# use the normal (global) Anki profile/base; still via uv
./start-anki.sh --global
```
The script passes Anki's `-b` flag to set the base directory (where `addons21/` resides) and `-p` if `ANKI_PROFILE` is provided. With `--global` it omits those flags so Anki uses the default global profile and base.

## Packaging and Releasing Add-ons

To move an add-on to the Anki add-on directory and create a zip file for uploading to AnkiWeb, you can use the provided `release.py` script. It has a `BASE` constant near the top that defaults to this repo's `_data` directory, so releases land in `_data/addons21/`:

```bash
uv run python release.py
```

The add-on will be moved to `addons21` inside the `BASE/` directory (see `BASE` in `release.py`). Start Anki from the `BASE/` directory with `-b <BASE>` argument following `anki` binary.

## Link

You can find my shared items on AnkiWeb at the following link:

[My shared items](https://ankiweb.net/shared/by-author/959135849)

Specific add-ons can be found in this profile.

## Contributing

Feel free to contribute by submitting issues or pull requests.
