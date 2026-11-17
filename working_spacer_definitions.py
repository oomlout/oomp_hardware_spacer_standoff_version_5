"""Attach editable drawing and CAD dictionaries to declared parts."""
import copy
import math
from hardware_model_render import presentation_defaults


def add_definitions(**kwargs):
    part = kwargs["part"]
    depth = part.get("depth_mm", 10)
    view_scales = kwargs.get("view_scales", [
        0.5,
        1,
        1.5,
        2,
        2.5,
        3,
        4,
        5,
        6,
    ])
    overall = part.get("overall_length_mm", depth)
    family = part.get("taxonomy_2", "spacer")
    thread_size = part.get("nominal_size", "m3").upper() if family == "standoff" else "M3"

    outside_width = part.get("outer_diameter_mm", 7) if family == "spacer" else part.get("across_flats_mm", 6) * 2 / math.sqrt(3)
    maximum_scale = max(0.5, min(90 / overall, 44 / outside_width))

    drawing = {}
    drawing["svg_name"] = "spacer_standoff_drawing"
    drawing["filename"] = "working_mechanical_drawing"
    drawing["sheet_width_mm"] = 210
    drawing["sheet_height_mm"] = 297
    drawing["font_family"] = "DejaVu Sans"
    drawing["ink"] = "#1a1a1a"
    drawing["muted"] = "#777777"
    drawing["accent"] = "#245b61"
    drawing["view_scale"] = max(value for value in view_scales if value <= maximum_scale)
    drawing["line_width_mm"] = 0.45
    drawing["dimension_font_mm"] = 3.2
    part["svg_details"] = drawing

    model = {}
    model["family"] = family
    model["depth_mm"] = depth
    model["bore_mm"] = part.get("bore_mm", 3.2)
    model["outer_diameter_mm"] = part.get("outer_diameter_mm", 7)
    model["across_flats_mm"] = part.get("across_flats_mm", 6)
    model["thread_nominal_diameter_mm"] = part.get("thread_nominal_diameter_mm", 3)
    model["thread_pitch_mm"] = part.get("thread_pitch_mm", 0.5)
    model["connection_type"] = part.get("connection_type", "plain")
    model["stud_length_mm"] = part.get("stud_length_mm", 0)
    model["tapped_depth_mm"] = part.get("tapped_depth_mm", 0)
    model["overall_length_mm"] = overall
    model["thread_model"] = part.get("thread_model", "none")
    model["edge_chamfer_mm"] = 0.12
    model["mouth_chamfer_mm"] = 0.2
    model["angular_segments"] = 96
    model["samples_per_pitch"] = 16
    model["finish"] = "nylon_white"
    model["specification"] = "Generic catalogue geometry"
    model["characteristic_dimension_mm"] = max(overall, model["outer_diameter_mm"], outside_width)
    model["characteristic_dimension_basis"] = "Maximum overall length or nominal outside width"

    recipe = {}
    recipe["schema_version"] = 1
    recipe["generator"] = "spacer_model_geometry"
    recipe["parameters"] = model
    recipe["notes"] = [
        part["dimension_status"],
        part["dimension_note"],
        "Small edge and mouth chamfers are illustrative assumptions, not measured supplier features.",
        f"Full standoff models have helical basic {thread_size} profiles; display models use smooth minor-diameter tapped bores and major-diameter studs.",
        "STL is in millimetres. GLB is in metres with Y up. OpenSCAD is in millimetres.",
    ]
    recipe.update(presentation_defaults(finish="nylon_white", family=family, elongated=overall > 12))
    recipe["studio"]["high_samples"] = 96
    recipe["renders"]["high"]["pixels"] = 1600
    recipe["renders"]["product_high"]["pixels"] = 1600
    part["three_d_model"] = recipe

    cad = copy.deepcopy(model)
    cad["oobb_type"] = family
    cad["oobb_name"] = family
    cad["run_scad"] = True
    cad["run_solidcraft"] = False
    part["oobb_type"] = family
    part["oobb_details"] = cad
