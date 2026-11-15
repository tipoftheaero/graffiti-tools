# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Mini snap/friction cap for a 400 mL aerosol can (Build123d).

Z=0 is the open end; Z=24 is the closed top. Units: millimeters.
Test-fit without forcing or actuating any valve; compatibility varies by can.

Import build() from the graffiti-tools build pipeline, or run this script to
export STEP and STL beside the source file.
"""

from pathlib import Path

from build123d import (
    Align,
    Box,
    Cylinder,
    GeomType,
    Pos,
    Rot,
    export_step,
    export_stl,
    fillet,
)

# Primary dimensions (mm)
inner_diameter = 32.5
wall_thickness = 1.0
top_thickness = 1.0
overall_height = 24.0
top_edge_radius = 0.7

# Four short inward gripping pads near the open rim
bump_count = 4
bump_projection = 0.5
bump_width = 4.0
bump_height = 1.5
bump_bottom_z = 0.75
bump_embed = 0.5
bump_edge_radius = 0.2


def build():
    """Return a single solid containing the shell and four gripping pads."""
    r_in = inner_diameter / 2.0
    r_out = r_in + wall_thickness

    # Put both cylinders' bottom faces at Z=0.
    shell = Cylinder(
        radius=r_out,
        height=overall_height,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cavity = Cylinder(
        radius=r_in,
        height=overall_height - top_thickness,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    cap = shell - cavity

    # Select exactly the outer top circular rim, not the underside of the lid.
    top_edges = [
        edge
        for edge in cap.edges()
        if edge.geom_type == GeomType.CIRCLE and abs(edge.center().Z - overall_height) < 1e-6
    ]
    if len(top_edges) != 1:
        raise RuntimeError(f"Expected one upper circular edge; found {len(top_edges)}")
    cap = fillet(top_edges, radius=top_edge_radius)

    pad_radial_size = bump_projection + bump_embed
    pad_center_r = r_in + (bump_embed - bump_projection) / 2.0
    pad_center_z = bump_bottom_z + bump_height / 2.0

    # Round each pad before fusing it to the cap, like the CadQuery original.
    basic_pad = Box(pad_radial_size, bump_width, bump_height)
    basic_pad = fillet(basic_pad.edges(), radius=bump_edge_radius)

    for i in range(bump_count):
        angle = i * 360.0 / bump_count
        pad = Rot(Z=angle) * Pos(pad_center_r, 0, pad_center_z) * basic_pad
        cap = cap + pad

    if not cap.is_valid:
        raise RuntimeError("Resulting cap is not a valid solid")
    if len(cap.solids()) != 1:
        raise RuntimeError(f"Expected one fused solid; found {len(cap.solids())}")
    return cap


if __name__ == "__main__":
    cap = build()
    output_dir = Path(__file__).resolve().parent
    step_file = output_dir / "spray_can_cover_mini.step"
    stl_file = output_dir / "spray_can_cover_mini.stl"

    export_step(cap, str(step_file))
    export_stl(cap, str(stl_file), tolerance=0.05, angular_tolerance=0.1)

    bounds = cap.bounding_box().size
    print("valid", cap.is_valid, "solids", len(cap.solids()))
    print("bounds", bounds.X, bounds.Y, bounds.Z)
    print("exported", step_file, stl_file)
    print("CAD valid:", cap.is_valid)
    print("CAD solids:", len(cap.solids()))
    print("CAD volume:", cap.volume)
