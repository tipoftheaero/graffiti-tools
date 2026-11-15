# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
"""Discover and validate printable tools from metadata. Standard library + PyYAML."""

from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def load_tool(folder: Path) -> dict:
    data = yaml.safe_load((folder / "tool.yaml").read_text(encoding="utf-8"))

    if not isinstance(data, dict):
        raise ValueError(f"{folder}: tool.yaml must be a mapping")
    required = ["id", "name", "version", "status", "cad", "dimensions"]

    for key in required:
        if key not in data:
            raise ValueError(f"{folder}: missing {key}")

    if data["id"] != folder.name:
        raise ValueError(f"{folder}: id must match directory")
    cad = data["cad"]

    if cad.get("engine") != "build123d" or cad.get("entrypoint") != "build":
        raise ValueError(f"{folder}: expected build123d build() contract")
    if not (folder / cad["source"]).is_file():
        raise ValueError(f"{folder}: CAD source not found")
    if set(cad.get("formats", [])) != {"stl", "step"}:
        raise ValueError(f"{folder}: release formats must be stl and step")
    if data["dimensions"].get("units") != "mm":
        raise ValueError(f"{folder}: dimensions must use mm")
    if not (folder / "README.md").exists():
        raise ValueError(f"{folder}: missing README.md")
    return data


def discover():
    return [
        (folder, load_tool(folder))
        for folder in sorted(TOOLS.iterdir())
        if folder.is_dir() and (folder / "tool.yaml").exists()
    ]


def select_tools(tool_id: str | None):
    tools = discover()

    if tool_id:
        tools = [(path, data) for path, data in tools if data["id"] == tool_id]

        if not tools:
            raise ValueError(f"Unknown tool: {tool_id}")
    return tools
