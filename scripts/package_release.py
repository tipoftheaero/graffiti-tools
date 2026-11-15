# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
"""Bundle generated artifacts and sources. Expects successful build + validate."""

import hashlib
import json
import zipfile
from pathlib import Path
from catalog import ROOT, select_tools


def zip_paths(dst: Path, files: list[tuple[Path, str]]):
    with zipfile.ZipFile(dst, "w", zipfile.ZIP_DEFLATED) as z:
        for path, arcname in files:
            z.write(path, arcname=arcname)


def main():
    release = ROOT / "release-assets"
    release.mkdir(exist_ok=True)
    tools = select_tools(None)

    for ext in ["stl", "step"]:
        files = [
            (ROOT / "dist" / data["id"] / f"{data['id']}.{ext}", f"{data['id']}/{data['id']}.{ext}")
            for folder, data in tools
        ]

        if any(not p.exists() for p, _ in files):
            raise RuntimeError("Missing builds: run build.py and validate.py")
        zip_paths(release / f"graffiti-tools-{ext}.zip", files)
    sources = []

    for folder, data in tools:
        for path in folder.rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                sources.append((path, str(path.relative_to(ROOT))))
    zip_paths(release / "graffiti-tools-sources.zip", sources)
    manifest = {
        "tools": [json.loads((ROOT / "dist" / d["id"] / "manifest.json").read_text()) for _, d in tools]
    }
    (release / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    checks = []

    for path in sorted(release.iterdir()):
        if path.is_file() and path.name != "SHA256SUMS.txt":
            checks.append(f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}")
    (release / "SHA256SUMS.txt").write_text("\n".join(checks) + "\n")
    print(f"Packaged {len(tools)} tools: {release}")


if __name__ == "__main__":
    main()
