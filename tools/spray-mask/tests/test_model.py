# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
import importlib.util
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "src" / "model.py"


def test_v6_model():
    spec = importlib.util.spec_from_file_location("spray_mask", SOURCE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    shape = module.build()
    bb = shape.bounding_box().size
    assert shape.is_valid
    assert shape.volume > 0
    assert abs(bb.X - 240) < 0.5
    assert abs(bb.Y - 174) < 0.5
    assert abs(bb.Z - 1.4) < 0.05
