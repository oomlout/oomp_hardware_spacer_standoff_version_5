"""Validate catalogue outputs, geometry, drawing pages and local links."""
import json
import re
from urllib.parse import unquote, urlsplit
import numpy as np
import trimesh
from pypdf import PdfReader
from PIL import Image
from oomp_populate_helper import build_oomp_id
from catalogue_io import ROOT, records, write_text


def main(**kwargs):
    part_filter = kwargs.get("filter", "*") or "*"
    report_path = kwargs.get("report_path", ROOT / "validation.json")
    failures = []
    results = []
    for folder, part in records(filter=part_filter):
        try:
            assert build_oomp_id(part) == folder.name == part["id"], "Taxonomy/folder identity mismatch"
            model = folder / "three_d_model"
            required = [
                "working.yaml", "README.md", "working_mechanical_drawing.svg",
                "working_mechanical_drawing.pdf", "working_mechanical_drawing.png",
                "label_oomp.svg", "scad/working.scad", "scad/working.stl",
                "three_d_model/model_full.stl", "three_d_model/model_display.stl",
                "three_d_model/model_full.glb", "three_d_model/model_display.glb",
                "three_d_model/parameters.json", "three_d_model/model.py",
                "three_d_model/studio.blend", "three_d_model/render_scene.json",
            ]
            for name in required:
                assert (folder / name).is_file(), f"Missing {name}"
            meshes = {}
            for variant in ["full", "display"]:
                mesh = trimesh.load(model / f"model_{variant}.stl", force="mesh")
                assert mesh.is_watertight and mesh.is_winding_consistent and mesh.volume > 0, f"Invalid {variant} STL"
                assert abs(mesh.extents[2] - part.get("overall_length_mm", part["depth_mm"])) < 0.0001, "Wrong overall length"
                if part["threaded"]:
                    lower = -part["stud_length_mm"] if "stud" in part["connection_type"] else 0
                    upper = part["depth_mm"] + (part["stud_length_mm"] if part["connection_type"] == "stud_to_stud" else 0)
                    assert np.allclose(mesh.bounds[:, 2], [lower, upper], atol=0.0001), "Stud/body endpoint mismatch"
                    assert abs(mesh.extents[1] - part["across_flats_mm"]) < 0.0001, "Wrong across-flats dimension"
                else:
                    assert abs(mesh.extents[0] - part["outer_diameter_mm"]) < 0.0001, "Wrong OD"
                glb = trimesh.load(model / f"model_{variant}.glb", force="scene")
                expected = mesh.extents[[0, 2, 1]] * 0.001
                assert np.allclose(glb.extents, expected, atol=1e-7), "GLB unit/axis mismatch"
                meshes[variant] = mesh
            scad = trimesh.load(folder / "scad/working.stl", force="mesh")
            assert scad.is_watertight and scad.volume > 0, "Invalid SCAD solid"
            assert np.allclose(scad.bounds, meshes["full"].bounds, atol=1e-5), "SCAD/mesh bounds differ"
            assert abs(scad.volume / meshes["full"].volume - 1) < 0.0001, "SCAD/mesh volumes differ"
            reader = PdfReader(folder / "working_mechanical_drawing.pdf")
            assert len(reader.pages) == 1, "Drawing must be one page"
            box = reader.pages[0].mediabox
            assert abs(float(box.width) * 25.4 / 72 - 210) < 0.02, "Drawing is not A4 width"
            assert abs(float(box.height) * 25.4 / 72 - 297) < 0.02, "Drawing is not A4 height"
            page_text = reader.pages[0].extract_text()
            assert f'DEPTH {part["depth_mm"]:g}' in page_text, "Depth annotation missing"
            assert f'{part["nominal_size"].upper()} x {part["depth_mm"]:g} mm' in page_text, "Screw-size heading missing"
            if part["threaded"]:
                assert part["thread"] in page_text, "Thread-size/pitch annotation missing"
            if not part["threaded"]:
                assert f'ID {part["bore_mm"]:g}' in page_text, "Bore annotation missing"
                assert f'OD {part["outer_diameter_mm"]:g}' in page_text, "OD annotation missing"
            if part.get("stud_length_mm", 0):
                assert f'OVERALL {part["overall_length_mm"]:g}' in page_text, "Overall annotation missing"
                assert f'STUD {part["stud_length_mm"]:g}' in page_text, "Stud annotation missing"
            recipe = json.loads((model / "parameters.json").read_text())
            assert recipe == part["three_d_model"], "Saved recipe differs from canonical metadata"
            from working_three_d_model import fingerprint
            build = json.loads((model / "build.json").read_text())
            assert build["fingerprint"] == fingerprint(recipe=recipe), "Model build is stale"
            assert build["rendered"], "Render pass is pending"
            scene = json.loads((model / "render_scene.json").read_text())
            assert scene["engine"] == "Cycles", "Unexpected renderer"
            assert scene["material"] == recipe["material"], "Render material differs from the recipe"
            for name, view in recipe["renders"].items():
                with Image.open(model / view["file"]) as image:
                    assert image.size == (view["pixels"], view["pixels"]), "Wrong render dimensions"
                    assert max(high-low for low,high in image.convert("RGB").getextrema()) > 30, "Blank render"
            for pose in scene["poses"].values():
                assert abs(pose["ground_clearance_mm"]) < 0.0001, "Floating model"
                assert all(frame["max_frame_fraction"] < 1 for frame in pose["framing"].values()), "Clipped model"
            results.append({"id": part["id"], "status": "passed", "volume_mm3": float(meshes["full"].volume)})
        except Exception as error:
            failures.append(f'{part["id"]}: {error}')
    # Validate Markdown/HTML local asset links in generated pages only.
    pages = [ROOT / "README.md"] + list((ROOT / "navigation_oobb").rglob("README.md")) + list((ROOT / "parts").glob("*/README.md"))
    for page in pages:
        if not page.exists():
            failures.append(f"Missing {page}")
            continue
        content = page.read_text(encoding="utf-8")
        content = re.sub(r"```.*?```", "", content, flags=re.S)
        links = re.findall(r'\]\(([^)]+)\)|(?:src|href)="([^"]+)"', content)
        for markdown, html in links:
            link = markdown or html
            parsed = urlsplit(link)
            if parsed.scheme or not parsed.path:
                continue
            target = page.parent / unquote(parsed.path)
            if not target.exists():
                failures.append(f"Broken link {page.relative_to(ROOT)}: {link}")
    report = {"parts_checked": len(results), "parts": results, "failures": failures}
    write_text(path=report_path, text=json.dumps(report, indent=2) + "\n")
    print(f"Validated {len(results)} parts; {len(failures)} failures")
    if failures:
        raise SystemExit("\n".join(failures))
    return report


if __name__ == "__main__":
    main()
