"""Catalogue contracts and geometric checks independent of rendered previews."""
import copy
import json
from pathlib import Path
from unittest.mock import patch
import numpy as np
import pytest
import yaml
from oomp_populate_helper import build_oomp_id
from working_oomp_populate_spacer import generate as spacers
from working_oomp_populate_standoff import generate as standoffs
from working_spacer_definitions import add_definitions
from spacer_model_geometry import build_model, internal_radius


def defined(part):
    add_definitions(part=part)
    return part


def test_declarations_are_independent_and_taxonomy_is_stable():
    parts = spacers() + standoffs()
    assert len(parts) == 157
    ids = [build_oomp_id(p) for p in parts]
    assert len(set(ids)) == 157
    assert all(p["taxonomy_1"] == "hardware" and p["taxonomy_3"] in ("m2_5", "m3", "m4", "m5", "m6") for p in parts)
    assert all(part_id.endswith("_mm_depth") for part_id in ids)
    parts[0]["source_refs"].append("changed")
    assert "changed" not in parts[1]["source_refs"]
    assert spacers()[0]["bore_mm"] == 3.2


@pytest.mark.parametrize("part", spacers(depths=[3,30]) + standoffs(depths=[6,30]))
def test_short_and_long_models_are_closed_and_dimensionally_correct(part):
    p = defined(part)["three_d_model"]["parameters"]
    full = build_model(parameters=p)
    display = build_model(parameters=p, variant="display")
    for mesh in (full, display):
        assert mesh.is_watertight
        assert mesh.is_winding_consistent
        assert mesh.volume > 0
        assert mesh.extents[2] == pytest.approx(part.get("overall_length_mm",part["depth_mm"]))
    if part["threaded"]:
        assert full.extents[1] == pytest.approx(part["across_flats_mm"])
        assert full.volume < display.volume
        assert len(full.faces) > len(display.faces)
    else:
        assert full.extents[0] == pytest.approx(part["outer_diameter_mm"])
        expected = np.pi / 4 * (part["outer_diameter_mm"]**2 - part["bore_mm"]**2) * part["depth_mm"]
        assert full.volume == pytest.approx(expected, rel=0.02)


def test_thread_profile_is_periodic_with_correct_major_minor_diameters():
    phase = np.linspace(0, 1, 1001)
    r = internal_radius(phase=phase)
    assert r.max() * 2 == pytest.approx(3)
    assert r.min() * 2 == pytest.approx(3 - 5 * np.sqrt(3) * 0.5 / 8)
    assert np.allclose(r, internal_radius(phase=phase + 1))
    assert not np.allclose(r, internal_radius(phase=phase + 0.25))


def test_invalid_geometry_is_rejected_before_export():
    p = defined(spacers()[0])["three_d_model"]["parameters"]
    p["bore_mm"] = 8
    with pytest.raises(ValueError, match="Bore"):
        build_model(parameters=p)


def test_manual_depths_and_filter_write_only_selected_parts(tmp_path, monkeypatch):
    import working_oomp_populate as populate
    monkeypatch.setattr(populate, "ROOT", tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "working_manual.yaml").write_text("options:\n  - type_name: spacer\n    depth_mm: 20\n")
    result = populate.main(filter="*_20_mm_depth")
    assert {p["taxonomy_2"] for p in result} == {"spacer", "standoff"}
    assert len(list((tmp_path / "parts_source").glob("*/working.yaml"))) == 19
    assert all(p["depth_mm"] == 20 for p in result)


def test_canonical_record_hash_and_links(tmp_path):
    import working_oomp
    from catalogue_io import write_yaml
    part = defined(spacers()[0])
    part_id = build_oomp_id(part)
    write_yaml(path=tmp_path / "sources" / part_id / "working.yaml", data=part)
    result = working_oomp.main(source_directory=tmp_path / "sources", output_directory=tmp_path / "parts")
    assert result[0]["id"] == part_id
    assert result[0]["directory"] == "parts/" + part_id
    assert "oomp_hardware_spacer_standoff_version_5" in result[0]["link_main"]
    assert len(result[0]["md5_6"]) == 6


def test_no_render_cache_cannot_hide_a_pending_render(tmp_path):
    import working_three_d_model as models
    part = defined(spacers()[0])
    with patch.object(models, "render_studio", side_effect=RuntimeError("renderer reached")):
        assert models.generate_assets(part=part, folder=tmp_path, render=False) == "built"
        # Even if old image names exist, rendered=False requires a new render.
        folder = tmp_path / "three_d_model"
        for name in [view["file"] for view in part["three_d_model"]["renders"].values()] + ["studio.blend", "render_scene.json", "readme_product.png", "readme_isometric.png"]:
            (folder / name).touch()
        with pytest.raises(RuntimeError, match="renderer reached"):
            models.generate_assets(part=part, folder=tmp_path, render=True)


def test_depth_navigation_uses_numeric_order():
    from working_readme import natural_key
    assert sorted(["10_mm_depth", "3_mm_depth", "25_mm_depth", "8_mm_depth"], key=natural_key) == ["3_mm_depth", "8_mm_depth", "10_mm_depth", "25_mm_depth"]


@pytest.mark.parametrize("connection", ["tapped_to_tapped", "stud_to_tapped", "stud_to_stud"])
def test_connection_layout_has_correct_cavities_and_solid_web(connection):
    part = standoffs(nominal_sizes=["m3"], depths=[6], connection_types=[connection])[0]
    p = defined(part)["three_d_model"]["parameters"]
    mesh = build_model(parameters=p)
    expected_bottom = -6 if "stud" in connection else 0
    expected_top = 12 if connection == "stud_to_stud" else 6
    assert mesh.bounds[:, 2] == pytest.approx([expected_bottom, expected_top])
    assert len(mesh.split()) == 1
    for z in [0.5, 3]:
        section = mesh.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        loops = len(section.discrete)
        expected = 2 if connection == "tapped_to_tapped" or (connection == "stud_to_tapped" and z > 1) else 1
        assert loops == expected
    if "stud" in connection:
        section = mesh.section(plane_origin=[0, 0, -3], plane_normal=[0, 0, 1])
        assert len(section.discrete) == 1
        assert max((section.vertices[:, :2]**2).sum(axis=1))**0.5 == pytest.approx(1.5)


def test_stud_profile_and_invalid_blind_tapping():
    from spacer_model_geometry import external_radius
    phase = np.linspace(0, 1, 1001)
    radius = external_radius(phase=phase)
    assert radius.max() == pytest.approx(1.5)
    assert radius.min() == pytest.approx(1.5 - 17*np.sqrt(3)*0.5/48)
    assert np.allclose(radius, external_radius(phase=phase+1))
    p = defined(standoffs(nominal_sizes=["m3"], depths=[6], connection_types=["stud_to_tapped"])[0])["three_d_model"]["parameters"]
    p["tapped_depth_mm"] = 6
    with pytest.raises(ValueError, match="solid web"):
        build_model(parameters=p)


def test_manual_connection_selects_only_the_requested_variant(tmp_path, monkeypatch):
    import working_oomp_populate as populate
    monkeypatch.setattr(populate, "ROOT", tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "working_manual.yaml").write_text("options:\n  - type_name: standoff\n    connection_type: stud_to_tapped\n    depth_mm: 18\n")
    result = populate.main(filter="*_18_mm_depth")
    assert len(result) == 1
    assert result[0]["connection_type"] == "stud_to_tapped"
    assert result[0]["overall_length_mm"] == 24


@pytest.mark.parametrize("size,bore,outside", [("m4",4.3,7),("m5",5.3,9),("m6",6.4,11)])
def test_new_spacer_series_have_one_diameter_and_correct_drawing_labels(size,bore,outside):
    from working_spacer_drawing import drawing_svg
    from working_readme import title
    parts = spacers(nominal_sizes=[size])
    assert len(parts) == 10
    assert {p["outer_diameter_mm"] for p in parts} == {outside}
    assert {p["bore_mm"] for p in parts} == {bore}
    assert {p["depth_mm"] for p in parts} == {3,5,6,8,10,12,15,20,25,30}
    for part in parts:
        defined(part)
        part["id"] = build_oomp_id(part)
        part["md5_6"] = "abcdef"
        svg = drawing_svg(part=part)
        assert f'{size.upper()} x {part["depth_mm"]:g} mm' in svg
        assert f'ID {bore:g} / PLAIN BORE' in svg
        assert f'OD {outside:g}' in svg
        assert title(part=part).startswith(size.upper())
        assert part["svg_details"]["view_scale"] * outside <= 44
        mesh = build_model(parameters=part["three_d_model"]["parameters"])
        section = mesh.section(plane_origin=[0,0,part["depth_mm"]/2],plane_normal=[0,0,1])
        assert len(section.discrete) == 2
        radii = sorted(np.sqrt((loop[:,:2]**2).sum(axis=1)).max() for loop in section.discrete)
        assert radii == pytest.approx([bore/2,outside/2])


def test_manual_spacer_size_is_preserved(tmp_path, monkeypatch):
    import working_oomp_populate as populate
    monkeypatch.setattr(populate,"ROOT",tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path/"working_manual.yaml").write_text("options:\n  - type_name: spacer\n    nominal_size: m5\n    depth_mm: 18\n")
    result = populate.main(filter="*_18_mm_depth")
    assert len(result) == 1
    assert result[0]["nominal_size"] == "m5"
    assert result[0]["outer_diameter_mm"] == 9
    assert result[0]["bore_mm"] == 5.3


@pytest.mark.parametrize("size,diameter,pitch,flats,stud", [
    ("m2.5", 2.5, 0.45, 5, 8),
    ("m4", 4, 0.7, 7, 6),
    ("m5", 5, 0.8, 10, 8),
    ("m6", 6, 1, 10, 10),
])
def test_metric_standoff_series_and_thread_annotations(size, diameter, pitch, flats, stud):
    from working_spacer_drawing import drawing_svg
    from spacer_model_geometry import external_radius
    parts = standoffs(nominal_sizes=[size])
    assert len(parts) == 24
    assert {p["depth_mm"] for p in parts} == {6, 8, 10, 12, 15, 20, 25, 30}
    assert {p["connection_type"] for p in parts} == {"tapped_to_tapped", "stud_to_tapped", "stud_to_stud"}
    for part in parts:
        defined(part)
        part["id"] = build_oomp_id(part)
        part["md5_6"] = "abcdef"
        assert part["taxonomy_3"] == size.replace(".", "_")
        assert part["across_flats_mm"] == flats
        assert part["thread_nominal_diameter_mm"] == diameter
        assert part["thread_pitch_mm"] == pitch
        count = part["connection_type"].count("stud")
        assert part["overall_length_mm"] == part["depth_mm"] + count * stud
        assert part["stud_length_mm"] == (stud if count else 0)
        svg = drawing_svg(part=part)
        assert f"{size.upper()} x {pitch:g}" in svg
        assert f"{size.upper()} x {part['depth_mm']:g} mm" in svg
        assert "M3 x 0.5" not in svg
        parameters = part["three_d_model"]["parameters"]
        assert parameters["thread_nominal_diameter_mm"] == diameter
        assert parameters["thread_pitch_mm"] == pitch
        if part["thread_model"] == "blind":
            assert 0 < part["tapped_depth_mm"] <= part["depth_mm"] - 1
    phase = np.linspace(0, 1, 1001)
    internal = internal_radius(phase=phase, diameter=diameter, pitch=pitch)
    external = external_radius(phase=phase, diameter=diameter, pitch=pitch)
    assert internal.max()*2 == pytest.approx(diameter)
    assert internal.min()*2 == pytest.approx(diameter - 5*np.sqrt(3)*pitch/8)
    assert external.max()*2 == pytest.approx(diameter)
    assert external.min()*2 == pytest.approx(diameter - 17*np.sqrt(3)*pitch/24)


@pytest.mark.parametrize("size", ["m2.5", "m2_5", "m4", "m5", "m6"])
def test_manual_standoff_size_is_preserved(tmp_path, monkeypatch, size):
    import working_oomp_populate as populate
    monkeypatch.setattr(populate, "ROOT", tmp_path)
    monkeypatch.chdir(tmp_path)
    (tmp_path / "working_manual.yaml").write_text(
        f"options:\n  - type_name: standoff\n    nominal_size: {size}\n    connection_type: stud_to_stud\n    depth_mm: 18\n"
    )
    result = populate.main(filter="*_18_mm_depth")
    assert len(result) == 1
    assert result[0]["nominal_size"] == size.replace("_", ".")
    assert result[0]["taxonomy_3"] == size.replace(".", "_")


def test_decimal_standoff_navigation_label_and_order():
    from working_readme import navigation_label, natural_key
    assert navigation_label("m2_5") == "M2.5"
    assert sorted(["m6", "m2_5", "m4", "m3", "m5"], key=natural_key) == ["m2_5", "m3", "m4", "m5", "m6"]
    with pytest.raises(ValueError, match="Standoff nominal size"):
        standoffs(nominal_sizes=["m2.7"])


def test_coincident_thread_samples_are_merged_before_meshing():
    from spacer_model_geometry import unique_heights
    heights = unique_heights(values=[0, 0.2, 0.20000000000000004, 5.8, 5.800000000000001, 6])
    assert heights == pytest.approx([0, 0.2, 5.8, 6])
