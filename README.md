# Anki Add-ons

This repository contains Anki add-ons and development utilities.

## Setting Up the Environment

Following instructions from [Intro & Downloads - Anki Betas](https://betas.ankiweb.net/#via-pypipip) to install Anki as Python package.

I use [Anaconda](https://www.anaconda.com/) to setup local Python 3.9 environment required for above.

```bash
conda create -n py39 python=3.9
conda activate py39
```

## Packaging and Releasing Add-ons

To move an add-on to the Anki add-on directory and create a zip file for uploading to AnkiWeb, you can use the provided `release.py` script:

```bash
python release.py
```

The add-on will be moved to `addons21` inside the `BASE/` directory that is configurable from `config.py`. Start Anki from the `BASE/` directory with `-b <BASE>` argument following `anki` binary.

## Link

You can find my shared items on AnkiWeb at the following link:

[My shared items](https://ankiweb.net/shared/by-author/959135849)

Specific add-ons can be found in this profile.

## Contributing

Feel free to contribute by submitting issues or pull requests.

