"""Refresh root, taxonomy navigation and canonical part documentation."""
from pathlib import Path
from string import Template
import os
import re
import shutil
import yaml
from catalogue_io import ROOT, records, write_text


def relative_link(**kwargs):
    source = kwargs["source"]
    target = kwargs["target"]
    return Path(os.path.relpath(target, source)).as_posix()


def natural_key(value):
    return tuple((0, int(item)) if item.isdigit() else (1, item) for item in re.split(r"(\d+)", value))


def navigation_label(value):
    if re.fullmatch(r"m\d+(?:_\d+)?", value):
        return value.replace("_", ".").upper()
    return value.replace("_", " ")


def title(**kwargs):
    part = kwargs["part"]
    depth = part["depth_mm"]
    if part["threaded"]:
        return f"{part['nominal_size'].upper()} x {depth:g} mm {part['connection_type'].replace('_', ' ')} hex standoff"
    return f"{part['nominal_size'].upper()} x {depth:g} mm round spacer"


def part_readme(**kwargs):
    folder = kwargs["folder"]
    part = kwargs["part"]
    sources = kwargs["sources"]
    dimensions = [
        ("Body depth", f"{part['depth_mm']:g} mm"),
        ("Material / colour", "Nylon / white"),
    ]
    if part["threaded"]:
        dimensions.extend([
            ("Thread, both ends", part["thread"]),
            ("Across flats", f"{part['across_flats_mm']:g} mm"),
            ("Connection", part["connection_type"]),
            ("Modelled thread construction", part["thread_model"]),
            ("Stud length, each", f"{part['stud_length_mm']:g} mm"),
            ("Modelled tapped depth", f"{part['tapped_depth_mm']:g} mm"),
            ("Overall length", f"{part['overall_length_mm']:g} mm"),
        ])
    else:
        dimensions.extend([
            ("Plain clearance bore", f"{part['bore_mm']:g} mm"),
            ("Outer diameter", f"{part['outer_diameter_mm']:g} mm"),
        ])
    table = "| Dimension | Value |\n| --- | --- |\n"
    for label, value in dimensions:
        table += f"| {label} | {value} |\n"
    images = []
    for path, label in [
        ("three_d_model/readme_isometric.png", "White nylon isometric render"),
        ("three_d_model/readme_product.png", "White nylon product render"),
        ("working_mechanical_drawing.png", "Dimensioned drawing"),
    ]:
        if (folder / path).exists():
            images.append(f'<a href="{path}"><img src="{path}" alt="{label}" width="280"></a>')
    downloads = []
    for path, label in [
        ("working.yaml", "OOMP metadata"),
        ("working_mechanical_drawing.svg", "Dimensioned SVG"),
        ("working_mechanical_drawing.pdf", "A4 dimensioned PDF"),
        ("label_oomp.svg", "Drawer label SVG"),
        ("scad/working.scad", "Editable OpenSCAD"),
        ("scad/working.stl", "OpenSCAD STL"),
        ("three_d_model/model_full.stl", "Full STL"),
        ("three_d_model/model_display.stl", "Display STL"),
        ("three_d_model/model_full.glb", "Full GLB"),
        ("three_d_model/model_display.glb", "Display GLB"),
        ("three_d_model/studio.blend", "Blender studio scene"),
        ("three_d_model/parameters.json", "Editable model recipe"),
        ("three_d_model/model.py", "Per-part model rebuild"),
        ("three_d_model/model_notes.md", "Model assumptions"),
        ("three_d_model/render_scene.json", "Lighting and render provenance"),
    ]:
        if (folder / path).exists():
            downloads.append(f"- [{label}]({path})")
    evidence = []
    for key in part["source_refs"]:
        source = sources[key]
        evidence.append(f'- [{source["title"]}]({source["url"]}): {source["supports"]} {source["limits"]}')
    taxonomy = " / ".join(part[f"taxonomy_{i}"] for i in range(1, 16) if part.get(f"taxonomy_{i}"))
    template = Template((ROOT / "presentation/PART.template.md").read_text(encoding="utf-8"))
    rendered = template.substitute(
        title=title(part=part),
        summary=f"White nylon spacing hardware for {part['nominal_size'].upper()} assemblies.",
        family=part["taxonomy_2"],
        images="\n".join(images),
        part_id=part["id"],
        taxonomy=taxonomy,
        dimensions=table,
        status=part["dimension_status"],
        note=part["dimension_note"],
        evidence="\n".join(evidence),
        downloads="\n".join(downloads),
        checked=max(sources[key].get("checked", "2026-11-16") for key in part["source_refs"]),
        metadata=yaml.safe_dump(part, sort_keys=False, allow_unicode=True).rstrip(),
    )
    target = folder / "README.md"
    start = "<!-- hardware-part:start -->"
    end = "<!-- hardware-part:end -->"
    if target.exists():
        old = target.read_text(encoding="utf-8")
        if old.count(start) != 1 or old.count(end) != 1 or old.index(end) < old.index(start):
            raise ValueError(f"Malformed generated section: {target}")
        rendered = old[:old.index(start)] + rendered.strip() + old[old.index(end)+len(end):]
    write_text(path=target, text=rendered.rstrip() + "\n")
    preview = folder / "three_d_model/readme_product.png"
    if preview.exists():
        shutil.copyfile(preview, folder / "image.png")


def navigation(**kwargs):
    entries = kwargs["entries"]
    tree = {}
    for folder, part in entries:
        path = ROOT / "navigation_oobb"
        segments = [part[f"taxonomy_{i}"] for i in range(1, 16) if part.get(f"taxonomy_{i}")]
        for segment in segments:
            child = path / segment
            tree.setdefault(path, {})[segment] = child
            path = child
        canonical = relative_link(source=path, target=folder / "README.md")
        write_text(path=path / "README.md", text=f'# {title(part=part)}\n\n[Up](../README.md)\n\n[Open canonical part record]({canonical})\n')
    for path, children in tree.items():
        lines = ["# " + ("Hardware catalogue" if path.name == "navigation_oobb" else navigation_label(path.name).title()), ""]
        root_link = relative_link(source=path, target=ROOT / "README.md")
        lines.extend([f"[Catalogue overview]({root_link})" + (" | [Up](../README.md)" if path.name != "navigation_oobb" else ""), ""])
        for segment in sorted(children, key=natural_key):
            lines.append(f'- [{navigation_label(segment)}]({segment}/README.md)')
        write_text(path=path / "README.md", text="\n".join(lines) + "\n")


def main(**kwargs):
    entries = records()
    sources = yaml.safe_load((ROOT / "source_file/dimension/sources.yaml").read_text(encoding="utf-8"))["sources"]
    for folder, part in entries:
        part_readme(folder=folder, part=part, sources=sources)
    navigation(entries=entries)
    template = Template((ROOT / "presentation/README.template.md").read_text(encoding="utf-8"))
    gallery = []
    for family in ["spacer", "standoff"]:
        for folder, part in entries:
            if part["taxonomy_2"] == family and part["depth_mm"] == 10 and (family == "spacer" or part["nominal_size"] == "m3" or part["connection_type"] == "stud_to_tapped"):
                image = folder / "three_d_model/readme_isometric.png"
                if image.exists():
                    path = folder.relative_to(ROOT).as_posix()
                    gallery.append(f'[<img src="{path}/three_d_model/readme_isometric.png" alt="{title(part=part)}, white nylon" width="360">]({path}/README.md)')
    depths = {}
    for family in ["spacer", "standoff"]:
        values = sorted({part["depth_mm"] for _, part in entries if part["taxonomy_2"] == family})
        depths[family] = ", ".join(f"{value:g}" for value in values)
    spacer_rows = []
    sizes = sorted({part["nominal_size"] for _, part in entries if part["taxonomy_2"] == "spacer"}, key=natural_key)
    for size in sizes:
        matching = [part for _, part in entries if part["taxonomy_2"] == "spacer" and part["nominal_size"] == size]
        outside = {part["outer_diameter_mm"] for part in matching}
        bores = {part["bore_mm"] for part in matching}
        if len(outside) != 1 or len(bores) != 1:
            raise ValueError(f"Expected one spacer diameter series for {size}")
        depth_list = ", ".join(f"{value:g}" for value in sorted({part["depth_mm"] for part in matching}))
        spacer_rows.append(f'| Round {size.upper()} clearance spacer, {next(iter(outside)):g} mm OD / {next(iter(bores)):g} mm bore | {depth_list} | [{size.upper()} spacers](navigation_oobb/hardware/spacer/{size}/README.md) |')
    standoff_rows = []
    standoff_sizes = sorted({part["nominal_size"] for _, part in entries if part["taxonomy_2"] == "standoff"}, key=natural_key)
    for size in standoff_sizes:
        for connection in ["tapped_to_tapped", "stud_to_tapped", "stud_to_stud"]:
            matching = [part for _, part in entries if part["taxonomy_2"] == "standoff" and part["nominal_size"] == size and part["connection_type"] == connection]
            if not matching:
                continue
            sample = matching[0]
            depth_list = ", ".join(f"{value:g}" for value in sorted({part["depth_mm"] for part in matching}))
            stud_detail = f', {sample["stud_length_mm"]:g} mm studs' if sample["stud_length_mm"] else ""
            standoff_rows.append(f'| {size.upper()} {connection.replace("_", " ")} hex standoff, {sample["across_flats_mm"]:g} mm A/F{stud_detail} | {depth_list} | [{connection}](navigation_oobb/hardware/standoff/{sample["taxonomy_3"]}/{connection}/README.md) |')
    write_text(path=ROOT / "README.md", text=template.substitute(
        count=len(entries),
        gallery="\n".join(gallery),
        spacer_rows="\n".join(spacer_rows),
        standoff_rows="\n".join(standoff_rows),
    ))


if __name__ == "__main__":
    main()
