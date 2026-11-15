# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
"""Validate metadata and built solids, sizes and STL meshes."""

import argparse
import json
import trimesh
from build123d import import_step
from catalog import ROOT, select_tools


def validate(folder, data):
    directory = ROOT / "dist" / data["id"]
    manifest_path = directory / "manifest.json"

    if not manifest_path.is_file():
        raise ValueError(f"{data['id']}: missing build artifacts; run build.py first")
    m = json.loads(manifest_path.read_text())

    for file in m["files"]:
        if not (directory / file).is_file():
            raise ValueError(f"{data['id']}: missing {file}")

    for axis, expected in [("x", "expected_width"), ("y", "expected_height"), ("z", "expected_thickness")]:
        actual = m["bounding_box_mm"][axis]

        if abs(actual - data["dimensions"][expected]) > data["dimensions"]["tolerance"]:
            raise ValueError(f"{data['id']}: bad {axis}: {actual} vs {data['dimensions'][expected]}")
    mesh = trimesh.load(str(directory / f"{data['id']}.stl"), force="mesh", process=True)

    if not mesh.is_watertight or not mesh.is_volume:
        raise ValueError(f"{data['id']}: STL is not a watertight volume")
    step = import_step(str(directory / f"{data['id']}.step"))

    if not step.is_valid or step.volume <= 0:
        raise ValueError(f"{data['id']}: STEP round trip failed")
    print(f"Validated {data['id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool")
    args = parser.parse_args()

    for folder, data in select_tools(args.tool):
        validate(folder, data)
