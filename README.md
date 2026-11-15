# Graffiti Tools

**Tip of the Aero** - open-source 3D printable graffiti and mural tools.

[Documentation](https://tipoftheaero.github.io/graffiti-tools/) · [Releases](https://github.com/tipoftheaero/graffiti-tools/releases) · [Report a problem](https://github.com/tipoftheaero/graffiti-tools/issues)

## Designs

| Tool | Status | CAD | Documentation |
|---|---|---|---|
| Spray Masking Shield V6 | Prototype | Build123d | [Tool README](tools/spray-mask/README.md) |

## Developer quick start

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,docs]'
python scripts/verify_catalog.py
pytest -q
python scripts/build.py
python scripts/validate.py
python scripts/package_release.py
mkdocs serve
```

- CAD source and metadata are committed; generated STL/STEP files are created by CI.
- Push a `vX.Y.Z` tag to create a GitHub Release after testing.
- `dist/`, `release-assets/`, and `site/` are ignored.
- The current Build123d port and complete CI have **not yet been runtime-tested in this scaffold environment**. Verify your first Actions run before tagging a release.

## Intellectual property

Licenses for CAD, code, photographs and documentation are **not yet selected**. See [LICENSES.md](LICENSES.md). Do not assume that publicly visible source is automatically licensed for reuse.
