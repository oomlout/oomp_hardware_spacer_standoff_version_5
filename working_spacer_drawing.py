"""A4 sheets following the bolt catalogue's header, views and dimension strip."""
import math
from html import escape
import subprocess
import shutil
from catalogue_io import records, write_text


def text(**kwargs):
    x = kwargs.get("x", 14)
    y = kwargs.get("y", 14)
    value = kwargs.get("value", "")
    size = kwargs.get("size", 3.2)
    anchor = kwargs.get("anchor", "start")
    colour = kwargs.get("colour", "#1a1a1a")
    weight = kwargs.get("weight", "normal")
    rotation = kwargs.get("rotation", 0)
    return f'<text x="{x}" y="{y}" fill="{colour}" stroke="none" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" transform="rotate({rotation} {x} {y})">{escape(str(value))}</text>'


def line(**kwargs):
    a = kwargs["a"]
    b = kwargs["b"]
    dash = kwargs.get("dash", "")
    return f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke-dasharray="{dash}"/>'


def dimension(**kwargs):
    a = kwargs["a"]
    b = kwargs["b"]
    label = kwargs["label"]
    vertical = kwargs.get("vertical", False)
    size = kwargs.get("size", 3.2)
    result = line(a=a, b=b)
    angle = math.atan2(b[1] - a[1], b[0] - a[0])
    for point, direction in [(a, 1), (b, -1)]:
        x, y = point
        ux = math.cos(angle) * direction
        uy = math.sin(angle) * direction
        coords = [(x, y), (x + ux * 2 - uy * 0.6, y + uy * 2 + ux * 0.6), (x + ux * 2 + uy * 0.6, y + uy * 2 - ux * 0.6)]
        result += '<polygon fill="#1a1a1a" points="' + ' '.join(f'{x},{y}' for x, y in coords) + '"/>'
    result += text(x=(a[0]+b[0])/2 + (5 if vertical else 0), y=(a[1]+b[1])/2 - (0 if vertical else 3), value=label, size=size, anchor="middle", rotation=-90 if vertical else 0)
    return result


def drawing_svg(**kwargs):
    part = kwargs["part"]
    settings = part["svg_details"]
    depth = part["depth_mm"]
    threaded = part["threaded"]
    connection = part.get("connection_type", "plain")
    stud = part.get("stud_length_mm", 0)
    overall = part.get("overall_length_mm", depth)
    scale = settings["view_scale"]
    width = part["across_flats_mm"] if threaded else part["outer_diameter_mm"]
    bore = part["thread_nominal_diameter_mm"] if threaded else part["bore_mm"]
    cx = 54
    sx = 151
    cy = 153
    radius = width * scale / math.sqrt(3) if threaded else width * scale / 2
    bore_radius = bore * scale / 2
    half_depth = depth * scale / 2
    family = "HEX STANDOFF / " + connection.replace("_", " ").upper() if threaded else "ROUND CLEARANCE SPACER"
    result = [f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="297mm" viewBox="0 0 210 297"><title>{escape(part["id"])}</title>',
        '<rect width="210" height="297" fill="white"/>',
        f'<g font-family="{settings["font_family"]}" stroke="{settings["ink"]}" stroke-width="{settings["line_width_mm"]}" fill="none">',
        '<rect x="4" y="4" width="202" height="289" rx="3.5"/>',
        text(y=15, value="OOMLOUT / OOMP", colour=settings["muted"]),
        text(x=196, y=15, value=part["md5_6"].upper(), anchor="end", colour=settings["muted"]),
        text(y=47, value=f'{part["nominal_size"].upper()} x {depth:g} mm', size=17, weight="bold"),
        text(y=59, value="HARDWARE / " + part["taxonomy_2"].upper(), size=4.5, colour=settings["muted"]),
        text(y=70, value=family + " / WHITE NYLON", size=3.5, colour=settings["muted"]),
        line(a=[14,79], b=[196,79]),
        text(y=88, value="DIMENSIONS", size=5.2, weight="bold"),
        text(x=196, y=88, value=f'{scale}:1 / mm / PRINT AT 100%', anchor="end", colour=settings["muted"]),
        text(x=cx, y=101, value="END VIEW", anchor="middle", weight="bold", colour=settings["muted"]),
        text(x=sx, y=101, value="SIDE VIEW", anchor="middle", weight="bold", colour=settings["muted"]),
    ]
    if threaded:
        points = [(cx+radius*math.cos(math.radians(90+60*i)), cy+radius*math.sin(math.radians(90+60*i))) for i in range(6)]
        result.append('<polygon fill="#fafafa" points="'+' '.join(f'{x},{y}' for x,y in points)+'"/>')
    else:
        result.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="#fafafa"/>')
    result.append(f'<circle cx="{cx}" cy="{cy}" r="{bore_radius}" fill="white"/>')
    if threaded:
        minor = (bore - (17 / 24 if connection == "stud_to_stud" else 5 / 8) * math.sqrt(3) * part["thread_pitch_mm"]) * scale / 2
        result.append(f'<circle cx="{cx}" cy="{cy}" r="{minor}" stroke-width="0.25"/>')
    # Side view looks normal to a hex flat; its silhouette is across corners.
    side_width = radius * 2 if threaded else width * scale
    left = sx - side_width / 2
    right = sx + side_width / 2
    overall_top = cy - overall * scale / 2
    overall_bottom = cy + overall * scale / 2
    top = overall_top + (stud * scale if connection == "stud_to_stud" else 0)
    bottom = top + depth * scale
    result.append(f'<rect x="{left}" y="{top}" width="{side_width}" height="{half_depth*2}" fill="#fafafa"/>')
    if threaded:
        for x in [sx-radius/2, sx+radius/2]:
            result.append(line(a=[x,top], b=[x,bottom]))
    if connection != "stud_to_stud":
        bore_bottom = top + part["tapped_depth_mm"] * scale if connection == "stud_to_tapped" else bottom
        for x in [sx-bore_radius,sx+bore_radius]:
            result.append(line(a=[x,top], b=[x,bore_bottom], dash="2 1"))
        if connection == "stud_to_tapped":
            result.append(line(a=[sx-bore_radius,bore_bottom], b=[sx+bore_radius,bore_bottom], dash="2 1"))
    stud_intervals = []
    if stud:
        stud_intervals.append((bottom,overall_bottom))
    if connection == "stud_to_stud":
        stud_intervals.append((overall_top,top))
    for start, end in stud_intervals:
        result.append(f'<rect x="{sx-bore_radius}" y="{start}" width="{bore_radius*2}" height="{end-start}" fill="#fafafa"/>')
        # Conventional thread lines: major outline, thin minor-diameter lines.
        minor = (bore - 17 * math.sqrt(3) * part["thread_pitch_mm"] / 24) * scale / 2
        for x in [sx-minor,sx+minor]:
            result.append(line(a=[x,start], b=[x,end]))
    if stud:
        result.append(dimension(a=[sx-bore_radius-7,bottom], b=[sx-bore_radius-7,overall_bottom], label="", vertical=True, size=2.8))
        result.append(text(x=sx-bore_radius-10, y=(bottom+overall_bottom)/2+1, value=f'STUD {stud:g}', anchor="end", size=2.8))
        for y in [bottom,overall_bottom]:
            result.append(line(a=[sx-bore_radius,y], b=[sx-bore_radius-9,y]))
        overall_x = right + 20
        for y in [overall_top,overall_bottom]:
            result.append(line(a=[sx+bore_radius,y], b=[overall_x+2,y]))
        result.append(dimension(a=[overall_x,overall_top], b=[overall_x,overall_bottom], label=f'OVERALL {overall:g}', vertical=True, size=2.8))
    result.append('<g stroke="#999999" stroke-width="0.2">')
    result.append(line(a=[cx-radius-4,cy], b=[cx+radius+4,cy], dash="5 1 1 1"))
    result.append(line(a=[cx,cy-radius-4], b=[cx,cy+radius+4], dash="5 1 1 1"))
    result.append(line(a=[sx,overall_top-4], b=[sx,overall_bottom+4], dash="5 1 1 1"))
    result.append('</g>')
    dimension_y = cy - radius - 9
    for x in [cx-width*scale/2,cx+width*scale/2]:
        result.append(line(a=[x,cy], b=[x,dimension_y-2]))
    result.append(dimension(a=[cx-width*scale/2,dimension_y], b=[cx+width*scale/2,dimension_y], label=f'{"A/F" if threaded else "OD"} {width:g}', size=settings["dimension_font_mm"]))
    dimension_x = right + 9
    for y in [top,bottom]:
        result.append(line(a=[right,y], b=[dimension_x+2,y]))
    result.append(dimension(a=[dimension_x,top], b=[dimension_x,bottom], label=f'DEPTH {depth:g}', vertical=True, size=settings["dimension_font_mm"]))
    # Bore callout sits below the end view, clear of the centre lines.
    result.append(line(a=[cx+bore_radius,cy], b=[cx+radius+5,cy+radius+10]))
    result.append(text(x=cx, y=cy+radius+18, value=(part["thread"] + " / STUD" if connection == "stud_to_stud" else part["thread"] + " / TAPPED") if threaded else f'ID {bore:g} / PLAIN BORE', anchor="middle", size=3.2))
    view_note = "HIDDEN BORE SHOWN DASHED"
    if connection == "stud_to_tapped":
        view_note = f'TAPPED DEPTH {part["tapped_depth_mm"]:g} mm / BLIND (ASSUMED)'
    if connection == "stud_to_stud":
        view_note = f'TWO STUDS / {stud:g} mm EACH / SOLID BODY'
    result.append(text(x=sx, y=211, value=view_note, anchor="middle", size=2.5, colour=settings["muted"]))
    result.append(line(a=[14,223], b=[196,223]))
    summaries = [
        (part["thread"] if threaded else f'{bore:g} mm', "THREAD" if threaded else "CLEARANCE ID"),
        (f'{width:g} mm', "ACROSS FLATS" if threaded else "OUTER DIAMETER"),
        (f'{depth:g} mm', "BODY DEPTH"),
        ("Nylon", "WHITE"),
    ]
    for index, (value, label) in enumerate(summaries):
        result.append(text(x=14+index*46, y=237, value=value, size=5, weight="bold"))
        result.append(text(x=14+index*46, y=245, value=label, size=2.8, colour=settings["muted"]))
    result.append(line(a=[14,253], b=[196,253]))
    result.append(text(y=261, value="GENERIC CATALOGUE DIMENSIONS / NOT A MANUFACTURING DRAWING", size=2.6, colour=settings["muted"]))
    model_note = f"{part['nominal_size'].upper()} screw clearance. Small model chamfers are illustrative."
    if connection == "tapped_to_tapped":
        model_note = "Through-thread model; supplier tapping depths vary."
    if connection == "stud_to_tapped":
        model_note = "Blind tapping and flat cavity floor are illustrative assumptions."
    if connection == "stud_to_stud":
        model_note = "Stud lengths exclude the hex body. Tip chamfers are illustrative."
    result.append(text(y=267, value=model_note, size=2.7))
    # Long taxonomy IDs wrap onto two lines without shrinking the main labels.
    words = part["id"].split("_")
    lines = [""]
    for word in words:
        if len(lines[-1]) + len(word) > 87:
            lines.append("")
        lines[-1] += ("_" if lines[-1] else "") + word
    for index, value in enumerate(lines):
        result.append(text(y=274+index*4, value=value, size=2.25, colour=settings["muted"]))
    result.append(text(y=287, value="OOMLOUT", size=2.6, colour=settings["accent"]))
    result.append(text(x=196, y=287, value="SOURCES AND MODEL NOTES IN PART README", anchor="end", size=2.4, colour=settings["muted"]))
    result.append('</g></svg>')
    return '\n'.join(result)


def export_pdf(**kwargs):
    source = kwargs["source"]
    destination = kwargs["destination"]
    from svglib.svglib import svg2rlg
    from reportlab.pdfgen import canvas
    from reportlab.graphics import renderPDF
    drawing = svg2rlg(str(source))
    pdf = canvas.Canvas(str(destination), pagesize=(drawing.width, drawing.height), invariant=1)
    renderPDF.draw(drawing, pdf, 0, 0)
    pdf.showPage()
    pdf.save()


def main(**kwargs):
    part_filter = kwargs.get("filter", "*") or "*"
    make_pdf = kwargs.get("make_pdf", True)
    make_png = kwargs.get("make_png", True)
    for folder, part in records(filter=part_filter):
        stem = folder / "working_mechanical_drawing"
        write_text(path=stem.with_suffix(".svg"), text=drawing_svg(part=part))
        label = '<svg xmlns="http://www.w3.org/2000/svg" width="76.2mm" height="50.8mm" viewBox="0 0 76.2 50.8"><rect width="76.2" height="50.8" fill="white"/><g font-family="DejaVu Sans">'
        label += text(x=4, y=7, value="OOMLOUT / " + part["taxonomy_2"].upper(), size=3)
        label += text(x=4, y=21, value=f'{part["nominal_size"].upper()} x {part["depth_mm"]:g}', size=10, weight="bold")
        label += text(x=4, y=30, value=part["connection_type"].replace("_", " ").upper() if part["threaded"] else f'{part["bore_mm"]:g} mm ID / {part["outer_diameter_mm"]:g} mm OD', size=2.8)
        label += text(x=4, y=38, value="WHITE NYLON", size=3.2)
        label += text(x=4, y=46, value=part["md5_6"].upper(), size=3)
        label += '</g></svg>'
        write_text(path=folder / "label_oomp.svg", text=label)
        if make_pdf or make_png:
            export_pdf(source=stem.with_suffix(".svg"), destination=stem.with_suffix(".pdf"))
        if make_png:
            executable = shutil.which("pdftoppm")
            if not executable:
                raise FileNotFoundError("Install Poppler (pdftoppm) to generate drawing previews")
            subprocess.run([executable, "-scale-to", "1400", "-singlefile", "-png", str(stem.with_suffix(".pdf")), str(stem)], check=True, capture_output=True)


if __name__ == "__main__":
    main()
