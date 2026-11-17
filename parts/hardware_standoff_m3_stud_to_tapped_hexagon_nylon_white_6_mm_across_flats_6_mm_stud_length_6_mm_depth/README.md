<!-- hardware-part:start -->
# M3 x 6 mm stud to tapped hex standoff

## Summary

White nylon spacing hardware for M3 assemblies.

[Catalogue overview](../../README.md) | [Browse family](../../navigation_oobb/hardware/standoff/README.md)

<a href="three_d_model/readme_isometric.png"><img src="three_d_model/readme_isometric.png" alt="White nylon isometric render" width="280"></a>
<a href="three_d_model/readme_product.png"><img src="three_d_model/readme_product.png" alt="White nylon product render" width="280"></a>
<a href="working_mechanical_drawing.png"><img src="working_mechanical_drawing.png" alt="Dimensioned drawing" width="280"></a>

Blender/Cycles reference renders from the saved CAD geometry; not product photographs.

## Details

**OOMP ID:** `hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth`

**Taxonomy:** hardware / standoff / m3 / stud_to_tapped / hexagon / nylon_white / 6_mm_across_flats / 6_mm_stud_length / 6_mm_depth

| Dimension | Value |
| --- | --- |
| Body depth | 6 mm |
| Material / colour | Nylon / white |
| Thread, both ends | M3 x 0.5 |
| Across flats | 6 mm |
| Connection | stud_to_tapped |
| Modelled thread construction | blind |
| Stud length, each | 6 mm |
| Modelled tapped depth | 5 mm |
| Overall length | 12 mm |


**Model basis:** Generic catalogue dimensions; not a manufacturer-specific drawing. Model uses a 6 mm stud and a 5 mm blind tapped cavity with a flat floor. Tapping is limited to body depth minus 1 mm to retain a solid web; this is an illustrative assumption, not verified usable engagement.

Small edge chamfers and material appearance are illustrative. Dimensions are nominal, with no supplier tolerances assigned. The full standoff mesh includes a helical basic thread; the display mesh uses smooth tapped bores and studs.

Source evidence checked 2026-11-16:

- [Lyn-Tron NY5172-06.0-00 nylon M3 stud-to-tapped standoff](https://www.lyntron.com/6.0mm-nylon-hexagon-male-female-standoff-unplated/pn/NY5172-06.0-00): Nylon M3 x 0.5 stud-to-tapped construction, 6 mm hex body width and 6 mm body depth. Family and body geometry evidence; the catalogue does not adopt a supplier-specific tapping depth or match every length.
- [RS PRO 6539504 nylon M3 stud-to-tapped standoff](https://us.rs-online.com/tools-hardware/hardware/standoff/?pg=318): Lists nylon M3 stud-to-tapped hardware with a 6 mm stud, in a 9 mm body example. Supports the stud-length choice only; not an exact SKU for the selected white nylon depth range.

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
across_flats_mm: 6
colour: white
connection_type: stud_to_tapped
depth_mm: 6
dimension_note: Model uses a 6 mm stud and a 5 mm blind tapped cavity with a flat
  floor. Tapping is limited to body depth minus 1 mm to retain a solid web; this is
  an illustrative assumption, not verified usable engagement.
dimension_status: Generic catalogue dimensions; not a manufacturer-specific drawing.
material: nylon
nominal_size: m3
oobb_details:
  across_flats_mm: 6
  angular_segments: 96
  bore_mm: 3.2
  characteristic_dimension_basis: Maximum overall length or nominal outside width
  characteristic_dimension_mm: 12
  connection_type: stud_to_tapped
  depth_mm: 6
  edge_chamfer_mm: 0.12
  family: standoff
  finish: nylon_white
  mouth_chamfer_mm: 0.2
  oobb_name: standoff
  oobb_type: standoff
  outer_diameter_mm: 7
  overall_length_mm: 12
  run_scad: true
  run_solidcraft: false
  samples_per_pitch: 16
  specification: Generic catalogue geometry
  stud_length_mm: 6
  tapped_depth_mm: 5
  thread_model: blind
  thread_nominal_diameter_mm: 3
  thread_pitch_mm: 0.5
oobb_type: standoff
overall_length_mm: 12
shape: hexagon
source_refs:
- lyntron_stud_tapped
- rs_stud_tapped
stud_length_mm: 6
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
tapped_depth_mm: 5
taxonomy_1: hardware
taxonomy_10: ''
taxonomy_11: ''
taxonomy_12: ''
taxonomy_13: ''
taxonomy_14: ''
taxonomy_15: ''
taxonomy_2: standoff
taxonomy_3: m3
taxonomy_4: stud_to_tapped
taxonomy_5: hexagon
taxonomy_6: nylon_white
taxonomy_7: 6_mm_across_flats
taxonomy_8: 6_mm_stud_length
taxonomy_9: 6_mm_depth
thread: M3 x 0.5
thread_model: blind
thread_nominal_diameter_mm: 3
thread_pitch_mm: 0.5
threaded: true
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
  - Model uses a 6 mm stud and a 5 mm blind tapped cavity with a flat floor. Tapping
    is limited to body depth minus 1 mm to retain a solid web; this is an illustrative
    assumption, not verified usable engagement.
  - Small edge and mouth chamfers are illustrative assumptions, not measured supplier
    features.
  - Full standoff models have helical basic M3 profiles; display models use smooth
    minor-diameter tapped bores and major-diameter studs.
  - STL is in millimetres. GLB is in metres with Y up. OpenSCAD is in millimetres.
  parameters:
    across_flats_mm: 6
    angular_segments: 96
    bore_mm: 3.2
    characteristic_dimension_basis: Maximum overall length or nominal outside width
    characteristic_dimension_mm: 12
    connection_type: stud_to_tapped
    depth_mm: 6
    edge_chamfer_mm: 0.12
    family: standoff
    finish: nylon_white
    mouth_chamfer_mm: 0.2
    outer_diameter_mm: 7
    overall_length_mm: 12
    samples_per_pitch: 16
    specification: Generic catalogue geometry
    stud_length_mm: 6
    tapped_depth_mm: 5
    thread_model: blind
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
taxonomy_2_upper: STANDOFF
taxonomy_2_upper_length_1: S
taxonomy_2_upper_length_2: ST
taxonomy_2_upper_length_3: STA
taxonomy_2_upper_length_4: STAN
taxonomy_2_upper_length_5: STAND
taxonomy_2_length_1: s
taxonomy_2_length_2: st
taxonomy_2_length_3: sta
taxonomy_2_length_4: stan
taxonomy_2_length_5: stand
taxonomy_2_capital: Standoff
taxonomy_2_first_letter: s
taxonomy_2_first_letter_upper: S
taxonomy_3_upper: M3
taxonomy_3_upper_length_1: M
taxonomy_3_upper_length_2: M3
taxonomy_3_upper_length_3: M3
taxonomy_3_upper_length_4: M3
taxonomy_3_upper_length_5: M3
taxonomy_3_length_1: m
taxonomy_3_length_2: m3
taxonomy_3_length_3: m3
taxonomy_3_length_4: m3
taxonomy_3_length_5: m3
taxonomy_3_capital: M3
taxonomy_3_first_letter: m
taxonomy_3_first_letter_upper: M
taxonomy_4_upper: STUD_TO_TAPPED
taxonomy_4_upper_length_1: S
taxonomy_4_upper_length_2: ST
taxonomy_4_upper_length_3: STU
taxonomy_4_upper_length_4: STUD
taxonomy_4_upper_length_5: STUD_
taxonomy_4_length_1: s
taxonomy_4_length_2: st
taxonomy_4_length_3: stu
taxonomy_4_length_4: stud
taxonomy_4_length_5: stud_
taxonomy_4_capital: Stud To Tapped
taxonomy_4_first_letter: s
taxonomy_4_first_letter_upper: S
taxonomy_5_upper: HEXAGON
taxonomy_5_upper_length_1: H
taxonomy_5_upper_length_2: HE
taxonomy_5_upper_length_3: HEX
taxonomy_5_upper_length_4: HEXA
taxonomy_5_upper_length_5: HEXAG
taxonomy_5_length_1: h
taxonomy_5_length_2: he
taxonomy_5_length_3: hex
taxonomy_5_length_4: hexa
taxonomy_5_length_5: hexag
taxonomy_5_capital: Hexagon
taxonomy_5_first_letter: h
taxonomy_5_first_letter_upper: H
taxonomy_6_upper: NYLON_WHITE
taxonomy_6_upper_length_1: N
taxonomy_6_upper_length_2: NY
taxonomy_6_upper_length_3: NYL
taxonomy_6_upper_length_4: NYLO
taxonomy_6_upper_length_5: NYLON
taxonomy_6_length_1: n
taxonomy_6_length_2: ny
taxonomy_6_length_3: nyl
taxonomy_6_length_4: nylo
taxonomy_6_length_5: nylon
taxonomy_6_capital: Nylon White
taxonomy_6_first_letter: n
taxonomy_6_first_letter_upper: N
taxonomy_7_upper: 6_MM_ACROSS_FLATS
taxonomy_7_upper_length_1: '6'
taxonomy_7_upper_length_2: '6_'
taxonomy_7_upper_length_3: 6_M
taxonomy_7_upper_length_4: 6_MM
taxonomy_7_upper_length_5: 6_MM_
taxonomy_7_length_1: '6'
taxonomy_7_length_2: '6_'
taxonomy_7_length_3: 6_m
taxonomy_7_length_4: 6_mm
taxonomy_7_length_5: 6_mm_
taxonomy_7_capital: 6 mm Across Flats
taxonomy_7_first_letter: '6'
taxonomy_7_first_letter_upper: '6'
taxonomy_8_upper: 6_MM_STUD_LENGTH
taxonomy_8_upper_length_1: '6'
taxonomy_8_upper_length_2: '6_'
taxonomy_8_upper_length_3: 6_M
taxonomy_8_upper_length_4: 6_MM
taxonomy_8_upper_length_5: 6_MM_
taxonomy_8_length_1: '6'
taxonomy_8_length_2: '6_'
taxonomy_8_length_3: 6_m
taxonomy_8_length_4: 6_mm
taxonomy_8_length_5: 6_mm_
taxonomy_8_capital: 6 mm Stud Length
taxonomy_8_first_letter: '6'
taxonomy_8_first_letter_upper: '6'
taxonomy_9_upper: 6_MM_DEPTH
taxonomy_9_upper_length_1: '6'
taxonomy_9_upper_length_2: '6_'
taxonomy_9_upper_length_3: 6_M
taxonomy_9_upper_length_4: 6_MM
taxonomy_9_upper_length_5: 6_MM_
taxonomy_9_length_1: '6'
taxonomy_9_length_2: '6_'
taxonomy_9_length_3: 6_m
taxonomy_9_length_4: 6_mm
taxonomy_9_length_5: 6_mm_
taxonomy_9_capital: 6 mm Depth
taxonomy_9_first_letter: '6'
taxonomy_9_first_letter_upper: '6'
id: hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
id_no_class: hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
id_no_type: hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
id_no_size: hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
oomp_key: oomp_hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
link_github: https://github.com/oomlout/oomp_hardware_spacer_standoff_version_5/tree/main/parts/hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
link_main: https://github.com/oomlout/oomp_hardware_spacer_standoff_version_5/tree/main/parts/hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
link_redirect: https://github.com/oomlout/oomp_hardware_spacer_standoff_version_5/tree/main/parts/hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
directory: parts/hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
name: hardware_standoff_m3_stud_to_tapped_hexagon_nylon_white_6_mm_across_flats_6_mm_stud_length_6_mm_depth
name_no_class: Hardware Standoff M3 Stud To Tapped Hexagon Nylon White 6 Mm Across
  Flats 6 Mm Stud Length 6 Mm Depth
name_no_type: Hardware Standoff M3 Stud To Tapped Hexagon Nylon White 6 Mm Across
  Flats 6 Mm Stud Length 6 Mm Depth
name_no_size: Hardware Standoff M3 Stud To Tapped Hexagon Nylon White 6 Mm Across
  Flats 6 Mm Stud Length 6 Mm Depth
md5: 7e3631d602c37eef8a1ecd94a9206c9f
md5_5: 7e363
md5_5_upper: 7E363
md5_6: 7e3631
md5_6_upper: 7E3631
md5_6_alpha: 4xa9d
md5_6_alpha_upper: 4XA9D
md5_10: 7e3631d602
md5_10_upper: 7E3631D602
bip_39_full_array:
- lawsuit
- ranch
- intact
- airport
- dawn
- jelly
- chronic
- super
- net
- empower
- brass
- dish
bip_39_full_space: lawsuit ranch intact airport dawn jelly chronic super net empower
  brass dish
bip_39_full_no_space: lawsuitranchintactairportdawnjellychronicsupernetempowerbrassdish
bip_39_full_underscore: lawsuit_ranch_intact_airport_dawn_jelly_chronic_super_net_empower_brass_dish
bip_39_2_word_array:
- lawsuit
- ranch
bip_39_2_word_space: lawsuit ranch
bip_39_2_word_no_space: lawsuitranch
bip_39_2_word_underscore: lawsuit_ranch
bip_39_3_word_array:
- lawsuit
- ranch
- intact
bip_39_3_word_space: lawsuit ranch intact
bip_39_3_word_no_space: lawsuitranchintact
bip_39_3_word_underscore: lawsuit_ranch_intact
name_space: hardware standoff m3 stud to tapped hexagon nylon white 6 mm across flats
  6 mm stud length 6 mm depth
name_proper: Hardware Standoff M3 Stud To Tapped Hexagon Nylon White 6 Mm Across Flats
  6 Mm Stud Length 6 Mm Depth
```

</details>

## Assembly

Select the depth required by the assembly. Match the nominal screw size and check the purchased part's actual clearance or usable thread engagement. No tested assembly procedure or tightening torque has been established for this generic record.
<!-- hardware-part:end -->
