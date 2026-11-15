#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
"""Run the graffiti-tools quality checks in order."""

import argparse
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STEPS = [
    ("Catalog", [sys.executable, "scripts/verify_catalog.py"]),
    ("Lint", [sys.executable, "-m", "ruff", "check", "."]),
    ("Format", [sys.executable, "-m", "ruff", "format", "--check", "."]),
    ("Build", [sys.executable, "scripts/build.py"]),
    ("Validate", [sys.executable, "scripts/validate.py"]),
    ("Tests", [sys.executable, "-m", "pytest", "-q"]),
]


def main():
    parser = argparse.ArgumentParser(description="Run all graffiti-tools checks.")
    parser.add_argument(
        "--skip-lint",
        action="store_true",
        help="Skip Ruff lint and formatting checks.",
    )
    args = parser.parse_args()

    started = time.monotonic()

    for name, command in STEPS:
        if args.skip_lint and name in ("Lint", "Format"):
            continue

        print(f"\n{'=' * 60}", flush=True)
        print(f"Running: {name}", flush=True)
        print(f"{'=' * 60}", flush=True)

        result = subprocess.run(command, cwd=ROOT, check=False)

        if result.returncode != 0:
            print(
                f"\nFAILED: {name} (exit {result.returncode})",
                file=sys.stderr,
            )
            return result.returncode

    elapsed = time.monotonic() - started

    print(f"\nAll checks passed in {elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
