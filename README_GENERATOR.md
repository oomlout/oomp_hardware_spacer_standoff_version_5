# Generator and maintenance guide

[Catalogue](README.md) | [Taxonomy navigation](navigation_oobb/README.md)

## Editing style

Keep declarations verbose and easy to edit: `option = {}` followed by one `option["field"] = value` per line, an explicit multiline depth list, and `copy.deepcopy` when appending a variant. Public catalogue routines accept `**kwargs` and resolve defaults at the top. Do not compress these declarations into clever comprehensions or a new framework.

## Pipeline

1. `working_oomp_populate_spacer.py` and `working_oomp_populate_standoff.py` declare families and depths. `working_spacer_definitions.py` attaches drawing, model and presentation dictionaries.
2. `working_oomp_populate.py` writes `parts_source/<id>/working.yaml` using the shared OOMP helper. Optional additional depths come from `working_manual.yaml`.
3. `working_oomp.py` makes canonical records in `parts/<id>/working.yaml`, using OOMP's identifiers and hashes. It finishes synchronously and corrects legacy base-repository URLs to this catalogue.
4. `working_svg.py` delegates to `working_spacer_drawing.py` for dimensioned SVG/PDF/PNG sheets and 76.2 x 50.8 mm drawer labels.
5. `working_scad.py` delegates to `working_spacer_scad.py` for portable, parameterized OpenSCAD files and optional STL exports.
6. `working_three_d_model.py` builds full/display STL and GLB models and Blender/Cycles renders. It uses the bolt project's locally copied studio/pose code. Each part receives an editable JSON recipe, rebuild script, `.blend` scene and render provenance.
7. `working_action.py` calls `working_readme.py` after all assets. Root templates live in `presentation/`; generated part sections preserve text outside their explicit markers. Navigation folders contain links to canonical assets, not duplicate geometry.

The existing generic OOBB/SolidCraft scaffolding is retained for future types, but these two hardware families explicitly select the SCAD route and disable native SolidCraft. No STEP output is claimed. Normal catalogue builds do not require SolidCraft, CorelDRAW, AI image generation or the sibling bolt checkout.

## Setup

Python 3.12 is the tested interpreter. Install `requirements.txt`, plus the shared OOMP core from [oomlout_oomp_version_5](https://github.com/oomlout/oomlout_oomp_version_5), so `oomp` and `oomp_populate_helper` are importable. The active SCAD route needs only this repository and the listed dependencies. Inherited OOBB recipe functions import their optional helpers only when called.

Install Blender 4.5 or newer, OpenSCAD and Poppler (`pdftoppm`) on PATH. Blender can also be selected with `OOMP_BLENDER_EXE`. Tested here with Blender 5.2 and the installed OpenSCAD nightly. The first run may take several minutes for studio renders; unchanged model recipes and source fingerprints are cached.

```powershell
python -m pip install -r requirements.txt
python working.py                  # complete catalogue, without duplicate SCAD STL export
python action_make_all.py           # also export OpenSCAD STL
python action_make_all_no_stl.py    # omit new STL exports; existing files stay
python action_documentation.py      # docs only, no CAD or rendering
python working_oomp_populate.py
python working_oomp.py
python working_svg.py
python working_scad.py
python working_three_d_model.py --filter '*_10_mm_depth'
python working_three_d_model.py --no-render
python -m pytest -q
python working_validate.py
python -m webserver.app
```

Filtered builds use the same glob at every asset stage. Documentation always refreshes the complete existing catalogue so a filtered build cannot hide other parts:

```powershell
python -c "import working; working.main(filter='*_10_mm_depth')"
```

`python parts/<id>/three_d_model/model.py` rebuilds one part from its adjacent `parameters.json`. Changes there are local experiments; promote permanent changes into the declaration/definition functions, since a catalogue regeneration replaces the saved recipe. For drawing and model consistency, edit the source declarations first and run the pipeline. The independent SCAD source is also manually editable with variables at its top.

## Taxonomy and file ownership

Spacers: `hardware / spacer / <nominal_size> / nylon_white / <od>_mm_outer_diameter / <depth>_mm_depth`. The editable `series_definitions` dictionaries in `working_oomp_populate_spacer.py` choose exactly one OD per screw size: M3 = 7 mm, M4 = 7 mm, M5 = 9 mm and M6 = 11 mm. Each has its own explicit bore, depth list and source references. Manual spacer entries use `type_name: spacer`, `nominal_size: m4`, and `depth_mm: 18`; omitted nominal_size remains M3 for compatibility.

Standoffs: `hardware / standoff / <nominal_size> / <connection_type> / hexagon / nylon_white / <width>_mm_across_flats / [<stud>_mm_stud_length /] <depth>_mm_depth`. `working_oomp_populate_standoff.series_definitions()` contains the editable diameter, pitch, flats, stud length and tapping choices for M2.5, M3, M4, M5 and M6. M2.5 uses `m2_5` in taxonomy and IDs, matching the bolt catalogue, and `m2.5` for displayed nominal_size.

Connections are `tapped_to_tapped`, `stud_to_tapped` and `stud_to_stud`. The stud-length level appears only for stud variants. The editable depth list is shared by all three. Manual entries can specify `type_name: standoff`, `nominal_size: m4`, `connection_type: stud_to_tapped`, and `depth_mm: 18`; omitting connection_type declares all three at that depth. Omitted nominal_size remains M3; both `m2.5` and `m2_5` inputs select the M2.5 series. Body depth excludes studs.

The family and nominal size follow the bolt/nut catalogue. Shape, connection type and finish precede dimensions; depth is last. Navigation sorts depths numerically. Do not rename an existing ID to alter its display order. Population updates declared records but never automatically deletes removed or manually maintained parts. Review and remove obsolete generated folders deliberately when changing taxonomy.

## Validation and provenance

`working_validate.py` checks metadata/taxonomy identity, expected artefacts, STL watertightness and positive volume, SCAD-vs-mesh dimensions/volume, GLB metre conversion, A4 page size and local documentation links. Tests cover independent declarations, filters, manual entries, thread geometry, regenerated metadata, and pipeline ordering. PDF previews come from Poppler, not an SVG screenshot. Visually inspect short and long parts whenever changing layout or camera settings.

Supplier evidence and explicitly limited assumptions are in [source_file/dimension](source_file/dimension/README.md). These are catalogue reference models, not fit-certified manufacturing drawings.
