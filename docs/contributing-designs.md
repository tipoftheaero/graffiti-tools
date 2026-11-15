# Contributing designs

Each tool belongs in `tools/<tool-id>/` with:

- `tool.yaml` describing name, source, CAD engine, version, expected bounds, print guidance, and test status
- `src/model.py` exposing `build()` returning a valid Build123d solid
- `README.md` with photos, print instructions, known limitations and compatibility
- `tests/test_model.py` with shape and parameter tests

Use millimeters and preserve source reproducibility. Add public-facing documentation under `docs/tools/` and update the MkDocs navigation.

License terms are pending selection by the repository owner; do not contribute third-party assets unless redistribution rights are documented.
