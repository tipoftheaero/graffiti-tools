# Spray Can Cover Mini — V1.1

**Status:** Prototype — no verified print fit or universal aerosol compatibility.

A small friction-fit cap intended to cover the valve area of a nominal 400 mL aerosol can. The cap has a closed top and four rounded internal gripping pads near the open rim. It must **never** be forced onto a can or fitted in a way that can press the valve.

## Design specification

| Property | Default |
|---|---:|
| Inner diameter | 32.5 mm |
| Nominal outer diameter | 34.5 mm |
| Overall height | 24.0 mm |
| Side wall | 1.0 mm |
| Closed top thickness | 1.0 mm |
| Upper exterior edge fillet | 0.7 mm |
| Number of gripping pads | 4 |
| Pad inward projection | 0.5 mm |
| Pad tangential width | 4.0 mm |
| Pad axial height | 1.5 mm |
| Pad bottom clearance | 0.75 mm |
| Pad embed into wall | 0.5 mm |
| Pad edge radius | 0.2 mm |

All dimensions are millimeters. `Z=0` is the open end; `Z=24` is the closed top. The body has a nominal 23 mm deep cavity. The four pads are spaced at 90° intervals.

## Files

- [`src/model.py`](src/model.py) — editable Build123d source, with a `build()` entrypoint
- [`tool.yaml`](tool.yaml) — metadata consumed by the shared build/validation pipeline
- [`tests/test_model.py`](tests/test_model.py) — geometry and parameter regression tests
- `dist/spray_can_cover_mini/` — generated STL/STEP/manifest from the shared build script (not committed)

## Build and validate

From the **repository root**, with the project's virtual environment active:

```bash
python scripts/verify_catalog.py
pytest -q tools/spray_can_cover_mini/tests
python scripts/build.py --tool spray_can_cover_mini
python scripts/validate.py --tool spray_can_cover_mini
```

The build outputs are expected under:

```text
dist/spray_can_cover_mini/
├── spray_can_cover_mini.stl
├── spray_can_cover_mini.step
└── manifest.json
```

You may also run `python tools/spray_can_cover_mini/src/model.py` to export the standalone V1.1 files beside the source. For a repository release, use the shared `scripts/build.py` workflow instead.

**Compatibility note:** The current shared scaffold expects Build123d `shape.is_valid` to be treated as a property (not `shape.is_valid()`) and STL export arguments `tolerance` / `angular_tolerance`. Apply those corrections to the existing shared scripts if not already fixed.

## Printing guidance (initial, unverified)

- Start with **PETG**, or PLA for an initial fit prototype.
- Try **0.4 mm nozzle**, **0.2 mm layers** and print open end down.
- A brim may help bed adhesion; inspect how the slicer handles the thin 1 mm walls and gripping pads.
- Avoid supports inside the cavity unless inspection shows they're required.
- Check the CAD and slicer preview to ensure the roof/top can be printed acceptably; adjust bridging or support settings as necessary.
- Test on a **non-actuated, stationary can**, with the nozzle/valve safely clear. Stop if there is resistance or contact with an actuator.

**Do not assume this works on all brands or valve configurations.** Document physical fit by can model and test conditions before marking it print-tested.

## Next steps

1. Confirm GitHub CI generates valid STL/STEP artifacts.
2. Print a PETG prototype, measure actual dimensions, and check safe clearance.
3. Add photographs and a measured compatibility table.
4. Parameterize fit variants only after physical testing.
