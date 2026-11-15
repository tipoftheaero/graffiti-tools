# Getting started

## Want to print?

1. Open the [Releases](https://github.com/tipoftheaero/graffiti-tools/releases) page.
2. Download the STL archive and extract the tool you want.
3. Import it into your slicer, review the tool's printing instructions, and inspect the thin-edge layers.

## Want to customize CAD?

Requires Python 3.11 and a supported desktop setup:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/build.py
python scripts/validate.py
```

Exports appear in `dist/`, which is intentionally gitignored.
