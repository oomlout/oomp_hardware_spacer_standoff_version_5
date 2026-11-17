"""Build catalogue meshes and reuse the bolt project's Blender studio."""
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image
from catalogue_io import ROOT, records, write_text
from spacer_model_geometry import build_model, export_glb
from hardware_model_render import render_studio


def fingerprint(**kwargs):
    recipe = kwargs["recipe"]
    digest = hashlib.sha256(json.dumps(recipe, sort_keys=True).encode())
    for name in [
        "spacer_model_geometry.py",
        "hardware_model_blender.py",
        "hardware_model_render.py",
        "hardware_model_pose.py",
        "working_three_d_model.py",
    ]:
        digest.update((ROOT / name).read_bytes())
    return digest.hexdigest()


def generate_assets(**kwargs):
    part = kwargs["part"]
    folder = Path(kwargs["folder"]) / "three_d_model"
    force = kwargs.get("force", False)
    render = kwargs.get("render", True)
    export_stl = kwargs.get("export_stl", True)
    recipe = part["three_d_model"]
    signature = fingerprint(recipe=recipe)
    folder.mkdir(parents=True, exist_ok=True)
    marker = folder / "build.json"
    previous = json.loads(marker.read_text()) if marker.exists() else {}
    expected = ["parameters.json", "model.py", "model_notes.md", "model_full.glb", "model_display.glb"]
    if export_stl:
        expected.extend(["model_full.stl", "model_display.stl"])
    if render:
        expected.extend([r["file"] for r in recipe["renders"].values()])
        expected.extend(["studio.blend", "render_scene.json", "readme_product.png", "readme_isometric.png"])
    if not force and previous.get("fingerprint") == signature and (not render or previous.get("rendered")) and all((folder / name).exists() for name in expected):
        return "cached"
    if previous.get("fingerprint") != signature:
        for name in [r["file"] for r in recipe["renders"].values()] + ["studio.blend", "render_scene.json", "readme_product.png", "readme_isometric.png"]:
            (folder / name).unlink(missing_ok=True)
        (folder.parent / "image.png").unlink(missing_ok=True)
    write_text(path=folder / "parameters.json", text=json.dumps(recipe, indent=2) + "\n")
    write_text(path=folder / "model_notes.md", text="# Model notes\n\n" + "\n\n".join(recipe["notes"]) + "\n")
    write_text(path=folder / "model.py", text='''"""Rebuild this part from the editable adjacent parameters.json."""
import json
from pathlib import Path
import sys

folder = Path(__file__).resolve().parent
sys.path.insert(0, str(folder.parents[2]))
from working_three_d_model import generate_assets

if __name__ == "__main__":
    recipe = json.loads((folder / "parameters.json").read_text(encoding="utf-8"))
    generate_assets(part={"three_d_model": recipe}, folder=folder.parent, force=True)
''')
    meshes = {}
    metrics = {}
    for variant in ["full", "display"]:
        mesh = build_model(parameters=recipe["parameters"], variant=variant)
        meshes[variant] = mesh
        export_glb(mesh=mesh, path=folder / f"model_{variant}.glb", material=recipe["material"])
        if export_stl:
            mesh.export(folder / f"model_{variant}.stl")
        metrics[variant] = {
            "watertight": bool(mesh.is_watertight),
            "volume_mm3": float(mesh.volume),
            "bounds_mm": mesh.bounds.tolist(),
            "faces": len(mesh.faces),
        }
    if render:
        # Blender itself resumes individual views, so explicitly invalidate
        # this part's known render files when geometry or settings change.
        for view in recipe["renders"].values():
            (folder / view["file"]).unlink(missing_ok=True)
        render_studio(meshes, recipe["parameters"], recipe, folder)
        for source, target in [
            ("render_high.png", "readme_isometric.png"),
            ("render_product_high.png", "readme_product.png"),
        ]:
            with Image.open(folder / source) as image:
                image.thumbnail((600, 600), Image.Resampling.LANCZOS)
                image.save(folder / target, optimize=True)
    result = {}
    result["fingerprint"] = signature
    result["metrics"] = metrics
    result["rendered"] = render
    write_text(path=marker, text=json.dumps(result, indent=2) + "\n")
    return "built"


def main(**kwargs):
    part_filter = kwargs.get("filter", "*") or "*"
    render = kwargs.get("render", True)
    force = kwargs.get("force", False)
    export_stl = kwargs.get("export_stl", True)
    results = []
    for folder, part in records(filter=part_filter):
        print(f"3D model: {part['id']}", flush=True)
        status = generate_assets(part=part, folder=folder, render=render, force=force, export_stl=export_stl)
        results.append({"id": part["id"], "status": status})
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--filter", default="*")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--no-render", action="store_true")
    args = parser.parse_args()
    main(filter=args.filter, force=args.force, render=not args.no_render)
