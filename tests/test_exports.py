# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
from pathlib import Path

import pytest
import trimesh
import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DIST = ROOT / "dist"


def discover_tools():
    """Find all registered CAD tools."""
    tools = []

    for metadata_file in sorted(TOOLS.glob("*/tool.yaml")):
        data = yaml.safe_load(metadata_file.read_text())

        tools.append(
            pytest.param(
                data["id"],
                id=data["id"],
            )
        )

    return tools


@pytest.mark.parametrize("tool_id", discover_tools())
def test_exported_stl(tool_id):
    """Every registered tool must export a valid STL."""

    path = DIST / tool_id / f"{tool_id}.stl"

    assert path.exists(), f"Missing STL for {tool_id}. Run python scripts/build.py first."

    mesh = trimesh.load(
        path,
        force="mesh",
        process=True,
    )

    assert mesh.is_watertight, f"{tool_id}: STL is not watertight"

    assert mesh.is_winding_consistent, f"{tool_id}: inconsistent face winding"

    assert mesh.is_volume, f"{tool_id}: STL is not a valid volume"

    assert len(mesh.split(only_watertight=False)) == 1, f"{tool_id}: expected exactly one connected mesh"
