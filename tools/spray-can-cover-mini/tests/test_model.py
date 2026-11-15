# SPDX-FileCopyrightText: 2026 Tip of the Aero contributors
# SPDX-License-Identifier: Apache-2.0
"""Regression tests for the mini spray can cover."""

import importlib.util
from pathlib import Path

import pytest

SOURCE = Path(__file__).resolve().parents[1] / "src" / "model.py"


def load_model():
    spec = importlib.util.spec_from_file_location("spray_can_cover_mini_model", SOURCE)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def model_and_shape():
    model = load_model()
    return model, model.build()


def test_valid_single_solid(model_and_shape):
    _, shape = model_and_shape
    assert shape.is_valid, "Mini cover should be a valid solid"
    assert len(shape.solids()) == 1, "Pads must fuse into the shell"
    assert shape.volume > 0


def test_envelope_dimensions(model_and_shape):
    model, shape = model_and_shape
    bb = shape.bounding_box().size
    expected_outer_diameter = model.inner_diameter + 2 * model.wall_thickness
    assert bb.X == pytest.approx(expected_outer_diameter, abs=0.05)
    assert bb.Y == pytest.approx(expected_outer_diameter, abs=0.05)
    assert bb.Z == pytest.approx(model.overall_height, abs=0.05)


def test_nominal_geometry_parameters(model_and_shape):
    model, _ = model_and_shape
    assert model.inner_diameter == 32.5
    assert model.bump_count == 4
    assert model.bump_projection == 0.5
    assert model.bump_bottom_z > 0
    assert model.bump_bottom_z + model.bump_height < model.overall_height - model.top_thickness
    assert 0 < model.top_edge_radius < model.wall_thickness


def test_gripping_pad_geometry(model_and_shape):
    _, shape = model_and_shape
    assert shape.is_valid
    assert len(shape.solids()) == 1
    assert abs(shape.bounding_box().size.Z - 24.0) < 0.01
