"""Watertight spacers and tapped/stud standoffs; lengths in millimetres."""
import math
import numpy as np
import trimesh


def validate_parameters(**kwargs):
    p = kwargs["parameters"]
    if p["family"] not in ("spacer", "standoff"):
        raise ValueError("Unknown hardware family")
    width = p["outer_diameter_mm"] if p["family"] == "spacer" else p["across_flats_mm"]
    hole = p["bore_mm"] if p["family"] == "spacer" else p["thread_nominal_diameter_mm"]
    if not 0 < hole < width or p["depth_mm"] <= 0:
        raise ValueError("Bore must fit inside a positive body")
    if not 0 <= p["edge_chamfer_mm"] < min(p["depth_mm"] / 2, (width - hole) / 4):
        raise ValueError("Edge chamfer consumes the body")
    if not 0 < p["mouth_chamfer_mm"] < min(p["depth_mm"] / 2, (width - hole) / 4):
        raise ValueError("Mouth chamfer consumes the wall")
    if p["thread_pitch_mm"] <= 0:
        raise ValueError("Thread pitch must be positive")
    if p["angular_segments"] < 24 or p["angular_segments"] % 12:
        raise ValueError("Angular segments must be a multiple of 12, at least 24")
    if p["samples_per_pitch"] < 8:
        raise ValueError("Threads require at least eight samples per pitch")
    if p["family"] == "standoff":
        connection = p["connection_type"]
        expected = {
            "tapped_to_tapped": "through",
            "stud_to_tapped": "blind",
            "stud_to_stud": "external_only",
        }
        if connection not in expected or p["thread_model"] != expected[connection]:
            raise ValueError("Connection and thread construction disagree")
        if "stud" in connection and p["stud_length_mm"] <= 2 * p["mouth_chamfer_mm"]:
            raise ValueError("Stud is too short for its tip chamfer")
        transition = p["mouth_chamfer_mm"] + 5 * math.sqrt(3) * p["thread_pitch_mm"] / 16
        if connection == "tapped_to_tapped" and 2 * transition >= p["depth_mm"]:
            raise ValueError("Thread entry transitions consume the body")
        if connection == "stud_to_tapped" and not transition < p["tapped_depth_mm"] < p["depth_mm"]:
            raise ValueError("Blind tapping must leave a solid web")
        overall = p["depth_mm"] + connection.count("stud") * p["stud_length_mm"]
        if not math.isclose(p["overall_length_mm"], overall):
            raise ValueError("Overall length disagrees with the studs and body")


def internal_radius(**kwargs):
    phase = np.asarray(kwargs["phase"])
    diameter = kwargs.get("diameter", 3)
    pitch = kwargs.get("pitch", 0.5)
    h = math.sqrt(3) * pitch / 2
    distance = np.abs((phase + 0.5) % 1 - 0.5)
    depth = np.clip((distance - 0.125) * pitch * math.sqrt(3), 0, 5 * h / 8)
    return (diameter - 5 * h / 4) / 2 + depth


def external_radius(**kwargs):
    phase = np.asarray(kwargs["phase"])
    diameter = kwargs.get("diameter", 3)
    pitch = kwargs.get("pitch", 0.5)
    distance = np.abs((phase + 0.5) % 1 - 0.5)
    depth = np.clip((distance - 0.0625) * pitch * math.sqrt(3), 0, 17 * math.sqrt(3) * pitch / 48)
    return diameter / 2 - depth


def unique_heights(**kwargs):
    values = np.unique(kwargs["values"])
    tolerance = kwargs.get("tolerance", 1e-8)
    # Merge coincident samples before vertex welding can collapse their faces.
    return values[np.r_[True, np.diff(values) > tolerance]]


def surface_rings(**kwargs):
    p = kwargs["parameters"]
    variant = kwargs.get("variant", "full")
    n = p["angular_segments"]
    length = p["depth_mm"]
    chamfer = p["edge_chamfer_mm"]
    mouth = p["mouth_chamfer_mm"]
    pitch = p["thread_pitch_mm"]
    threaded = p["family"] == "standoff"
    connection = p["connection_type"]
    stud = p["stud_length_mm"]
    diameter = p["thread_nominal_diameter_mm"] if threaded else p["bore_mm"]
    theta = np.arange(n) * 2 * math.pi / n
    rings = []

    def add_stud(start, end, tip):
        count = math.ceil(stud / pitch * p["samples_per_pitch"]) if variant == "full" else 1
        root_depth = 17 * math.sqrt(3) * pitch / 48
        tip_chamfer = mouth + root_depth
        transition = tip + tip_chamfer if tip == start else tip - tip_chamfer
        zs = unique_heights(values=np.r_[np.linspace(start, end, count + 1), transition])
        for z in zs:
            r = external_radius(phase=z / pitch - theta / (2 * math.pi), diameter=diameter, pitch=pitch) if variant == "full" else np.full(n, diameter / 2)
            r = np.minimum(r, diameter / 2 - tip_chamfer + abs(z - tip))
            rings.append((z, r))

    if "stud" in connection:
        add_stud(-stud, 0, -stud)
    body_radius = p["across_flats_mm"] / 2 / np.cos(theta % (math.pi / 3) - math.pi / 6) if threaded else np.full(n, p["outer_diameter_mm"] / 2)
    for z in unique_heights(values=[0, chamfer, length - chamfer, length]):
        rings.append((z, body_radius - max(0, chamfer - min(z, length - z))))
    if connection == "stud_to_stud":
        add_stud(length, length + stud, length + stud)
    # Follow the boundary down the bore after following the outside upward.
    # A through bore closes into a loop. A blind bore ends at a flat floor.
    through = not threaded or connection == "tapped_to_tapped"
    if connection != "stud_to_stud":
        low = 0 if through else length - p["tapped_depth_mm"]
        count = math.ceil((length - low) / pitch * p["samples_per_pitch"]) if threaded and variant == "full" else 1
        transition = mouth + (5 * math.sqrt(3) * pitch / 16 if threaded else 0)
        samples = [length - mouth, length - transition]
        if through:
            samples.extend([mouth, transition])
        zs = unique_heights(values=np.r_[np.linspace(low, length, count + 1), samples])[::-1]
        for z in zs:
            if threaded:
                r = internal_radius(phase=z / pitch - theta / (2 * math.pi), diameter=diameter, pitch=pitch) if variant == "full" else np.full(n, (diameter - 5 * math.sqrt(3) * pitch / 8) / 2)
            else:
                r = np.full(n, diameter / 2)
            distance = min(z, length - z) if through else length - z
            rings.append((z, np.maximum(r, diameter / 2 + mouth - distance)))
    return rings, through


def build_model(**kwargs):
    p = kwargs["parameters"]
    variant = kwargs.get("variant", "full")
    validate_parameters(parameters=p)
    if variant not in ("full", "display"):
        raise ValueError("Variant must be full or display")
    n = p["angular_segments"]
    theta = np.arange(n) * 2 * math.pi / n
    rings, closed = surface_rings(parameters=p, variant=variant)
    vertices = []
    faces = []
    for z, ring in rings:
        vertices.extend(np.column_stack((ring * np.cos(theta), ring * np.sin(theta), np.full(n, z))).tolist())
    for row in range(len(rings) if closed else len(rings) - 1):
        next_row = (row + 1) % len(rings)
        for col in range(n):
            a = row * n + col
            b = row * n + (col + 1) % n
            c = next_row * n + (col + 1) % n
            d = next_row * n + col
            faces.extend([[a, b, c], [a, c, d]])
    if not closed:
        bottom = len(vertices)
        vertices.extend([[0, 0, rings[0][0]], [0, 0, rings[-1][0]]])
        for col in range(n):
            nxt = (col + 1) % n
            last = (len(rings) - 1) * n
            faces.extend([[bottom, nxt, col], [bottom + 1, last + col, last + nxt]])
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=True)
    if not mesh.is_watertight or not mesh.is_winding_consistent or mesh.volume <= 0:
        raise ValueError("Model failed closed positive solid validation")
    return mesh


def export_glb(**kwargs):
    mesh = kwargs["mesh"].copy()
    path = kwargs["path"]
    material = kwargs["material"]
    mesh.apply_transform(np.array([
        [0.001, 0, 0, 0],
        [0, 0, 0.001, 0],
        [0, -0.001, 0, 0],
        [0, 0, 0, 1],
    ]))
    mesh.visual = trimesh.visual.TextureVisuals(material=trimesh.visual.material.PBRMaterial(
        name=material["name"],
        baseColorFactor=[round(c * 255) for c in material["base_colour_srgb"]] + [255],
        metallicFactor=material["metallic"],
        roughnessFactor=material["roughness"],
    ))
    scene = trimesh.Scene(mesh)
    scene.metadata["units"] = "metres"
    scene.metadata["source_units"] = "millimetres"
    scene.export(str(path))
