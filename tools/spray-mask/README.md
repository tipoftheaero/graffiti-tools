# Spray Masking Shield

**Status:** prototype / digitally validated only after CI succeeds. Not yet marked as physically print-tested.

Parametric-width-independent V6 geometry, currently 240 mm wide, with a 1.4 mm body and a 5 mm taper down to 0.6 mm on the curved top, right, and straight bottom edges. The left vertical edge is kept at full thickness except at its bottom corner.

## CAD source

- `src/model.py` - Build123d port of the original CadQuery V6 model.
- `tool.yaml` - machine-readable release and build metadata.

## Build locally

```bash
python scripts/build.py --tool spray-mask
python scripts/validate.py --tool spray-mask
```

Generated STEP/STL files appear under `dist/spray-mask/` and are not committed to source control. Release ZIPs are published under GitHub Releases.

## Print guidance (unverified)

- Suggested start: PETG, flat on build plate, 0.4 mm nozzle, 0.2 mm layers.
- This part has a thin 0.6 mm edge; inspect slicer previews for adequate toolpaths.
- Do a small test print and check edge flexibility before field use.
- Clean up sharp or rough printed edges. Do not use near flames or other ignition sources.

## Validation and changelog

- Automated: geometry, dimensions, export, watertight mesh checks.
- Physical: **not yet verified**. Add actual photographs, can compatibility and field test observations before marking tested.

## Attribution

Adapted from the supplied Spray Masking Shield V6 CadQuery design; rewritten for Build123d.
