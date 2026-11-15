# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
"""Build all registered tools into dist/<tool-id>/ (never commit dist)."""

import argparse
import hashlib
import importlib.util
import json
import trimesh

from build123d import export_step, export_stl
from catalog import ROOT, select_tools


def clean_stl(path, max_fragment_faces=2):
    """Remove tiny isolated mesh fragments, preserving the main solid."""
    mesh = trimesh.load(str(path), force="mesh", process=True)

    if mesh.is_volume:
        return

    parts = mesh.split(only_watertight=False)
    parts.sort(key=lambda part: len(part.faces), reverse=True)

    if not parts:
        raise ValueError(f"{path}: STL contains no geometry")

    main = parts[0]
    fragments = parts[1:]

    if not main.is_volume:
        raise ValueError(f"{path}: main mesh component is not a valid volume")

    if any(len(part.faces) > max_fragment_faces for part in fragments):
        raise ValueError(f"{path}: significant disconnected geometry detected")

    # Only discard fragments that are negligible compared with
    # the main component.
    fragment_area = sum(part.area for part in fragments)

    if fragment_area > main.area * 1e-5:
        raise ValueError(f"{path}: disconnected fragments exceed area threshold")

    if fragments:
        main.export(str(path))

    # Validate the actual output, not just the in-memory mesh.
    cleaned = trimesh.load(str(path), force="mesh", process=True)

    if not cleaned.is_watertight or not cleaned.is_volume:
        raise ValueError(f"{path}: STL cleanup did not produce a valid volume")

    print(f"Cleaned {path.name}: removed {len(fragments)} tiny fragments")


def generate(folder, data):
    path = folder / data["cad"]["source"]
    spec = importlib.util.spec_from_file_location(f"cad_{data['id'].replace('-', '_')}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    result = getattr(module, data["cad"]["entrypoint"])()

    if not result.is_valid or result.volume <= 0:
        raise RuntimeError(f"{data['id']}: geometry invalid or empty")
    output = ROOT / "dist" / data["id"]
    output.mkdir(parents=True, exist_ok=True)
    stl = output / f"{data['id']}.stl"
    step = output / f"{data['id']}.step"
    export_stl(
        result,
        str(stl),
        tolerance=0.01,
        angular_tolerance=0.05,
    )
    clean_stl(stl)
    export_step(result, str(step))
    bb = result.bounding_box().size
    manifest = {
        "id": data["id"],
        "name": data["name"],
        "version": data["version"],
        "status": data["status"],
        "units": "mm",
        "volume_mm3": result.volume,
        "bounding_box_mm": {"x": bb.X, "y": bb.Y, "z": bb.Z},
        "files": {
            p.name: {"bytes": p.stat().st_size, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in (stl, step)
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Built {data['id']} -> {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool", help="build just one tool ID")
    args = parser.parse_args()

    for folder, data in select_tools(args.tool):
        generate(folder, data)
