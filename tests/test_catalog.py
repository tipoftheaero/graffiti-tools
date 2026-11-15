# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from catalog import discover


def test_catalog():
    entries = discover()
    assert entries
    ids = [data["id"] for _, data in entries]
    assert len(ids) == len(set(ids))
