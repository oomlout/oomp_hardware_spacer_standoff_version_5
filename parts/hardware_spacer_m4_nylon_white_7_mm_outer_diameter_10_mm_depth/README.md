<!-- hardware-part:start -->
# M4 x 10 mm round spacer

## Summary

White nylon spacing hardware for M4 assemblies.

[Catalogue overview](../../README.md) | [Browse family](../../navigation_oobb/hardware/spacer/README.md)

<a href="three_d_model/readme_isometric.png"><img src="three_d_model/readme_isometric.png" alt="White nylon isometric render" width="280"></a>
<a href="three_d_model/readme_product.png"><img src="three_d_model/readme_product.png" alt="White nylon product render" width="280"></a>
<a href="working_mechanical_drawing.png"><img src="working_mechanical_drawing.png" alt="Dimensioned drawing" width="280"></a>

Blender/Cycles reference renders from the saved CAD geometry; not product photographs.

## Details

**OOMP ID:** `hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth`

**Taxonomy:** hardware / spacer / m4 / nylon_white / 7_mm_outer_diameter / 10_mm_depth

| Dimension | Value |
| --- | --- |
| Body depth | 10 mm |
| Material / colour | Nylon / white |
| Plain clearance bore | 4.3 mm |
| Outer diameter | 7 mm |


**Model basis:** Generic catalogue dimensions; not a manufacturer-specific drawing. M4 denotes screw compatibility; the plain clearance bore is 4.3 mm, not a thread. Outside diameter follows the user-specified catalogue series; supplier references support bore and depth choices only.

Small edge chamfers and material appearance are illustrative. Dimensions are nominal, with no supplier tolerances assigned. The full standoff mesh includes a helical basic thread; the display mesh uses smooth tapped bores and studs.

Source evidence checked 2026-11-17:

- [User-specified spacer outside diameters](../../source_file/dimension/README.md): User selected M4 = 7 mm OD, M5 = 9 mm OD and M6 = 11 mm OD, retaining M3 = 7 mm OD. Catalogue specification; no supplier SKU or claim of most-common online availability is established for these ODs.
- [Pencom metric spacer clearance bores and depth options](https://www.pencomsf.com/site/assets/product-catalogs/spacers/rsp-round-spacers-catalog.pdf): Documents 4.3/5.3/6.4 mm clearance bores, nylon options and the selected 3-30 mm depths. Used for bore and depth context only; its 8/10/13 mm OD series does not verify the selected 7/9/11 mm ODs.

## Parts

- [OOMP metadata](working.yaml)
- [Dimensioned SVG](working_mechanical_drawing.svg)
- [A4 dimensioned PDF](working_mechanical_drawing.pdf)
- [Drawer label SVG](label_oomp.svg)
- [Editable OpenSCAD](scad/working.scad)
- [OpenSCAD STL](scad/working.stl)
- [Full STL](three_d_model/model_full.stl)
- [Display STL](three_d_model/model_display.stl)
- [Full GLB](three_d_model/model_full.glb)
- [Display GLB](three_d_model/model_display.glb)
- [Blender studio scene](three_d_model/studio.blend)
- [Editable model recipe](three_d_model/parameters.json)
- [Per-part model rebuild](three_d_model/model.py)
- [Model assumptions](three_d_model/model_notes.md)
- [Lighting and render provenance](three_d_model/render_scene.json)

These formats describe the same part. STL/SCAD units are millimetres; GLB units are metres with Y up. The [part folder](./) contains all generated assets.

<details>
<summary>Complete OOMP metadata</summary>

```yaml
bore_mm: 4.3
colour: white
depth_mm: 10
dimension_note: M4 denotes screw compatibility; the plain clearance bore is 4.3 mm,
  not a thread. Outside diameter follows the user-specified catalogue series; supplier
  references support bore and depth choices only.
dimension_status: Generic catalogue dimensions; not a manufacturer-specific drawing.
material: nylon
nominal_size: m4
oobb_details:
  across_flats_mm: 6
  angular_segments: 96
  bore_mm: 4.3
  characteristic_dimension_basis: Maximum overall length or nominal outside width
  characteristic_dimension_mm: 10
  connection_type: plain
  depth_mm: 10
  edge_chamfer_mm: 0.12
  family: spacer
  finish: nylon_white
  mouth_chamfer_mm: 0.2
  oobb_name: spacer
  oobb_type: spacer
  outer_diameter_mm: 7
  overall_length_mm: 10
  run_scad: true
  run_solidcraft: false
  samples_per_pitch: 16
  specification: Generic catalogue geometry
  stud_length_mm: 0
  tapped_depth_mm: 0
  thread_model: none
  thread_nominal_diameter_mm: 3
  thread_pitch_mm: 0.5
oobb_type: spacer
outer_diameter_mm: 7
shape: round
source_refs:
- user_spacer_od_selection
- pencom_spacer_bores_depths
svg_details:
  accent: '#245b61'
  dimension_font_mm: 3.2
  filename: working_mechanical_drawing
  font_family: DejaVu Sans
  ink: '#1a1a1a'
  line_width_mm: 0.45
  muted: '#777777'
  sheet_height_mm: 297
  sheet_width_mm: 210
  svg_name: spacer_standoff_drawing
  view_scale: 6
taxonomy_1: hardware
taxonomy_10: ''
taxonomy_11: ''
taxonomy_12: ''
taxonomy_13: ''
taxonomy_14: ''
taxonomy_15: ''
taxonomy_2: spacer
taxonomy_3: m4
taxonomy_4: nylon_white
taxonomy_5: 7_mm_outer_diameter
taxonomy_6: 10_mm_depth
taxonomy_7: ''
taxonomy_8: ''
taxonomy_9: ''
threaded: false
three_d_model:
  generator: spacer_model_geometry
  material:
    base_colour_srgb:
    - 0.86
    - 0.85
    - 0.81
    coat_roughness: 0.28
    coat_weight: 0.025
    metallic: 0.0
    microtexture_height_um: 0.4
    microtexture_spacing_mm: 0.025
    name: Natural white nylon
    note: Visual natural nylon approximation; exact polymer grade and mould surface
      not supplied by catalogue.
    roughness: 0.38
    roughness_variation: 0.025
  notes:
  - Generic catalogue dimensions; not a manufacturer-specific drawing.
  - M4 denotes screw compatibility; the plain clearance bore is 4.3 mm, not a thread.
    Outside diameter follows the user-specified catalogue series; supplier references
    support bore and depth choices only.
  - Small edge and mouth chamfers are illustrative assumptions, not measured supplier
    features.
  - Full standoff models have helical basic M3 profiles; display models use smooth
    minor-diameter tapped bores and major-diameter studs.
  - STL is in millimetres. GLB is in metres with Y up. OpenSCAD is in millimetres.
  parameters:
    across_flats_mm: 6
    angular_segments: 96
    bore_mm: 4.3
    characteristic_dimension_basis: Maximum overall length or nominal outside width
    characteristic_dimension_mm: 10
    connection_type: plain
    depth_mm: 10
    edge_chamfer_mm: 0.12
    family: spacer
    finish: nylon_white
    mouth_chamfer_mm: 0.2
    outer_diameter_mm: 7
    overall_length_mm: 10
    samples_per_pitch: 16
    specification: Generic catalogue geometry
    stud_length_mm: 0
    tapped_depth_mm: 0
    thread_model: none
    thread_nominal_diameter_mm: 3
    thread_pitch_mm: 0.5
  renders:
    high:
      file: render_high.png
      pixels: 1600
      variant: full
      view: isometric
    low:
      file: render_low.png
      pixels: 512
      variant: display
      view: isometric
    product_high:
      file: render_product_high.png
      pixels: 1600
      variant: full
      view: product
    product_low:
      file: render_product_low.png
      pixels: 512
      variant: display
      view: product
  schema_version: 1
  studio:
    adaptive_threshold: 0.015
    denoise: true
    device: auto
    engine: cycles
    exposure: 0.0
    floor_colour_srgb:
    - 0.93
    - 0.935
    - 0.94
    floor_roughness: 0.55
    framing_margin: 0.13
    high_samples: 96
    lights:
    - colour:
      - 1.0
      - 0.96
      - 0.9
      height: 5.0
      name: Key softbox
      position:
      - -3
      - -4
      - 6
      power: 650.0
      width: 4.0
    - colour:
      - 0.9
      - 0.95
      - 1.0
      height: 4.0
      name: Fill softbox
      position:
      - 4
      - -1
      - 3
      power: 330.0
      width: 3.0
    - colour:
      - 1.0
      - 1.0
      - 1.0
      height: 5.0
      name: Rim strip
      position:
      - 1
      - 4
      - 4
      power: 850.0
      width: 1.2
    look: AgX - Medium High Contrast
    low_samples: 48
    poses:
      isometric:
        camera_eye:
        - 1
        - -1
        - 1
        orientation: principal axis Z up
        projection: orthographic
      product:
        camera_eye:
        - -6
        - -10
        - 6
        orientation: resting on lower face, bore visible
        projection: orthographic
        resting_axis: face
        support: Stable convex-hull support using actual mesh centre of mass.
        yaw_degrees: -12.0
    seed: 7991
    view_transform: AgX
    world_colour:
    - 0.78
    - 0.82
    - 0.9
    world_strength: 0.35
taxonomy_1_upper: HARDWARE
taxonomy_1_upper_length_1: H
taxonomy_1_upper_length_2: HA
taxonomy_1_upper_length_3: HAR
taxonomy_1_upper_length_4: HARD
taxonomy_1_upper_length_5: HARDW
taxonomy_1_length_1: h
taxonomy_1_length_2: ha
taxonomy_1_length_3: har
taxonomy_1_length_4: hard
taxonomy_1_length_5: hardw
taxonomy_1_capital: Hardware
taxonomy_1_first_letter: h
taxonomy_1_first_letter_upper: H
taxonomy_2_upper: SPACER
taxonomy_2_upper_length_1: S
taxonomy_2_upper_length_2: SP
taxonomy_2_upper_length_3: SPA
taxonomy_2_upper_length_4: SPAC
taxonomy_2_upper_length_5: SPACE
taxonomy_2_length_1: s
taxonomy_2_length_2: sp
taxonomy_2_length_3: spa
taxonomy_2_length_4: spac
taxonomy_2_length_5: space
taxonomy_2_capital: Spacer
taxonomy_2_first_letter: s
taxonomy_2_first_letter_upper: S
taxonomy_3_upper: M4
taxonomy_3_upper_length_1: M
taxonomy_3_upper_length_2: M4
taxonomy_3_upper_length_3: M4
taxonomy_3_upper_length_4: M4
taxonomy_3_upper_length_5: M4
taxonomy_3_length_1: m
taxonomy_3_length_2: m4
taxonomy_3_length_3: m4
taxonomy_3_length_4: m4
taxonomy_3_length_5: m4
taxonomy_3_capital: M4
taxonomy_3_first_letter: m
taxonomy_3_first_letter_upper: M
taxonomy_4_upper: NYLON_WHITE
taxonomy_4_upper_length_1: N
taxonomy_4_upper_length_2: NY
taxonomy_4_upper_length_3: NYL
taxonomy_4_upper_length_4: NYLO
taxonomy_4_upper_length_5: NYLON
taxonomy_4_length_1: n
taxonomy_4_length_2: ny
taxonomy_4_length_3: nyl
taxonomy_4_length_4: nylo
taxonomy_4_length_5: nylon
taxonomy_4_capital: Nylon White
taxonomy_4_first_letter: n
taxonomy_4_first_letter_upper: N
taxonomy_5_upper: 7_MM_OUTER_DIAMETER
taxonomy_5_upper_length_1: '7'
taxonomy_5_upper_length_2: '7_'
taxonomy_5_upper_length_3: 7_M
taxonomy_5_upper_length_4: 7_MM
taxonomy_5_upper_length_5: 7_MM_
taxonomy_5_length_1: '7'
taxonomy_5_length_2: '7_'
taxonomy_5_length_3: 7_m
taxonomy_5_length_4: 7_mm
taxonomy_5_length_5: 7_mm_
taxonomy_5_capital: 7 mm Outer Diameter
taxonomy_5_first_letter: '7'
taxonomy_5_first_letter_upper: '7'
taxonomy_6_upper: 10_MM_DEPTH
taxonomy_6_upper_length_1: '1'
taxonomy_6_upper_length_2: '10'
taxonomy_6_upper_length_3: '10_'
taxonomy_6_upper_length_4: 10_M
taxonomy_6_upper_length_5: 10_MM
taxonomy_6_length_1: '1'
taxonomy_6_length_2: '10'
taxonomy_6_length_3: '10_'
taxonomy_6_length_4: 10_m
taxonomy_6_length_5: 10_mm
taxonomy_6_capital: 10 mm Depth
taxonomy_6_first_letter: '1'
taxonomy_6_first_letter_upper: '1'
id: hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
id_no_class: hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
id_no_type: hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
id_no_size: hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
oomp_key: oomp_hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
link_github: https://github.com/oomlout/oomp_hardware_spacer_standoff_version_5/tree/main/parts/hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
link_main: https://github.com/oomlout/oomp_hardware_spacer_standoff_version_5/tree/main/parts/hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
link_redirect: https://github.com/oomlout/oomp_hardware_spacer_standoff_version_5/tree/main/parts/hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
directory: parts/hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
name: hardware_spacer_m4_nylon_white_7_mm_outer_diameter_10_mm_depth
name_no_class: Hardware Spacer M4 Nylon White 7 Mm Outer Diameter 10 Mm Depth
name_no_type: Hardware Spacer M4 Nylon White 7 Mm Outer Diameter 10 Mm Depth
name_no_size: Hardware Spacer M4 Nylon White 7 Mm Outer Diameter 10 Mm Depth
md5: 37574ac0610c169ecd01f0ece710c7e4
md5_5: '37574'
md5_5_upper: '37574'
md5_6: 37574a
md5_6_upper: 37574A
md5_6_alpha: 25qh6
md5_6_alpha_upper: 25QH6
md5_10: 37574ac061
md5_10_upper: 37574AC061
bip_39_full_array:
- dance
- ripple
- quote
- search
- scrap
- exhaust
- cross
- dignity
- undo
- decade
- cradle
- siren
bip_39_full_space: dance ripple quote search scrap exhaust cross dignity undo decade
  cradle siren
bip_39_full_no_space: danceripplequotesearchscrapexhaustcrossdignityundodecadecradlesiren
bip_39_full_underscore: dance_ripple_quote_search_scrap_exhaust_cross_dignity_undo_decade_cradle_siren
bip_39_2_word_array:
- dance
- ripple
bip_39_2_word_space: dance ripple
bip_39_2_word_no_space: danceripple
bip_39_2_word_underscore: dance_ripple
bip_39_3_word_array:
- dance
- ripple
- quote
bip_39_3_word_space: dance ripple quote
bip_39_3_word_no_space: danceripplequote
bip_39_3_word_underscore: dance_ripple_quote
name_space: hardware spacer m4 nylon white 7 mm outer diameter 10 mm depth
name_proper: Hardware Spacer M4 Nylon White 7 Mm Outer Diameter 10 Mm Depth
```

</details>

## Assembly

Select the depth required by the assembly. Match the nominal screw size and check the purchased part's actual clearance or usable thread engagement. No tested assembly procedure or tightening torque has been established for this generic record.
<!-- hardware-part:end -->
