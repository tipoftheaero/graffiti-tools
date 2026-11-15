# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Spray masking shield

Dimensions in mm.

Geometry preserved from the supplied source:
- 240-mm-wide profile using four sampled cubic Bezier curves
- 1.4-mm interior thickness, 0.6-mm perimeter thickness
- 5-mm taper along curved top, right edge and entire bottom edge
- left vertical edge remains untapered, apart from bottom corner transition

The sampled polygon edges are preserved rather than replaced with true Bezier
edges so the generated solid tracks the original geometry.
"""

import math

from build123d import Face, Solid, Vector, Wire

WIDTH = 240.0
MAX_THICKNESS = 1.4
EDGE_THICKNESS = 0.6
TAPER_WIDTH = 5.0
SAMPLES_PER_BEZIER = 28

BEZIERS = [
    [(0, 105), (0, 150), (35, 174), (69, 174)],
    [(69, 174), (103, 174), (119, 149), (132, 122)],
    [(132, 122), (147, 92), (175, 89), (196, 89)],
    [(196, 89), (224, 89), (240, 77), (240, 56)],
]


def bezier(ctrl, t):
    u = 1 - t
    return (
        u**3 * ctrl[0][0] + 3 * u**2 * t * ctrl[1][0] + 3 * u * t**2 * ctrl[2][0] + t**3 * ctrl[3][0],
        u**3 * ctrl[0][1] + 3 * u**2 * t * ctrl[1][1] + 3 * u * t**2 * ctrl[2][1] + t**3 * ctrl[3][1],
    )


def make_profiles():
    curve = []

    for segment in BEZIERS:
        for k in range(SAMPLES_PER_BEZIER + 1):
            if curve and k == 0:
                continue
            curve.append(bezier(segment, k / SAMPLES_PER_BEZIER))

    # Same vertex order/count as the CadQuery source, needed for ruled loft.
    outer = [(0, 0), (0, 105), *curve[1:], (WIDTH, 0)]
    inner = [(0, TAPER_WIDTH), (0, 105)]

    for i, (x, y) in enumerate(curve[1:], start=1):
        xa, ya = curve[max(0, i - 1)]
        xb, yb = curve[min(len(curve) - 1, i + 1)]
        dx, dy = xb - xa, yb - ya
        norm = math.hypot(dx, dy)
        nx, ny = dy / norm, -dx / norm
        fade = min(1.0, i / 12.0)
        inner.append((x + TAPER_WIDTH * fade * nx, y + TAPER_WIDTH * fade * ny))

    inner.append((WIDTH - TAPER_WIDTH, TAPER_WIDTH))
    return outer, inner


def polygon_wire(points, z):
    return Wire.make_polygon([Vector(x, y, z) for x, y in points], close=True)


def make_shield():
    outer, inner = make_profiles()
    lower_wire = polygon_wire(outer, 0)
    shoulder_wire = polygon_wire(outer, EDGE_THICKNESS)
    inner_wire = polygon_wire(inner, MAX_THICKNESS)

    # Flat bottom/perimeter layer, then the matching ruled taper.
    base = Solid.extrude(Face(lower_wire), Vector(0, 0, EDGE_THICKNESS))
    transition = Solid.make_loft([shoulder_wire, inner_wire], ruled=True)
    shield = base.fuse(transition)
    return shield.clean()


def build():
    """Return the default V6 spray mask solid (millimeters)."""
    return make_shield()
