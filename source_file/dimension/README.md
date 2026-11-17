# Dimension evidence and model choices

The dated source register is [sources.yaml](sources.yaml). These records describe generic catalogue parts, not certified reproductions of one supplier's SKU. The initial sources were checked on 16 November 2026; the additional standoff sources were checked on 17 November 2026; stock and prices are deliberately not recorded.

The M3 round spacer uses a 3.2 mm plain clearance bore and 7 mm OD. Soundtronics lists this geometry at 3, 5 and 8 mm lengths. Siqma's 10 mm product listing supplies another example. The remaining selected depths are common M3 spacer assortment sizes; the VXB reference is black nylon with a stated 3 mm bore and supports depth selection only. White nylon is the requested catalogue finish, not a claim of a matched SKU for every combination.

The additional round-spacer series use **M4: 8 mm OD / 4.3 mm bore**, **M5: 10 mm OD / 5.3 mm bore**, and **M6: 13 mm OD / 6.4 mm bore**. Each has 3, 5, 6, 8, 10, 12, 15, 20, 25 and 30 mm body depths. Exactly one OD series is populated per screw size.

These ODs were selected from repeated online catalogue families, not a sales-volume ranking. RAF/MW and Nyfast support the M4 8 mm section; Lyn-Tron and Bolt Base support the M5 10 mm section; RAF/MW and Lyn-Tron support the M6 13 mm section. Pencom pages 11-13 independently cover all three OD/bore combinations, nylon options and every selected body depth. Other M6 products use 10, 12.5 or 12.7 mm ODs; they are deliberately not added as competing series. Clearance holes vary slightly by supplier. The chosen bores follow common metric clearance dimensions rather than equating screw size with an exact-size hole. The requested white/natural nylon appearance is retained; these are generic models, not exact supplier reproductions or a claim that every white size is stocked.

The M3 tapped-to-tapped standoff uses a 6 mm hexagon across flats. CQRobot documents a white nylon family at several selected lengths; Lyn-Tron and Wurth support the 6 mm hex/M3 geometry. The initial 8, 12 and 25 mm depths are generic common catalogue selections, not exact SKU matches. Wurth's examples are black; their dimensions do not establish white material identity.

The basic thread is M3 x 0.5. Full models use ideal helical internal and external profiles, without fit allowance, thread runout, lead-in specification or tolerance class. The tapped-to-tapped model assumes a through thread. Wurth's 30 mm example instead specifies 10 mm tapping at either end: use the purchased part's drawing for engagement depth. Display models use the basic minor diameter as a smooth bore and the major diameter for smooth studs.

The 0.12 mm outer edge chamfer and 0.2 mm mouth transition are explicit visual assumptions. No polymer grade, strength, electrical rating or moulding tolerance is assigned. Changing these values is supported in the declaration/definition pipeline and the saved per-part model recipe.

M3 stud-to-tapped models use one 6 mm stud and a blind tapped cavity of `min(6, body_depth - 1)` mm, leaving a solid web at the stud root. The flat cavity floor and tapping depth are modelling assumptions, not guaranteed usable thread engagement. Lyn-Tron supports the nylon hex/M3 family; the RS PRO reference supports a 6 mm stud.

M3 stud-to-stud models use two 6 mm studs and a solid hex body. Essentra's catalogue includes an M3 / 6 mm body / 6 mm stud layout, but uses brass inserts in nylon. This catalogue deliberately models the requested all-nylon construction. The shared 6, 8, 10, 12, 15, 20, 25 and 30 mm body depths are a consistent catalogue range; exact all-nylon supplier availability has not been established for every depth.

Stud lengths exclude the body. Overall length equals body depth plus one or two stud lengths. Stud tips have an illustrative chamfer extending below the basic external thread root; no tool relief or fit tolerance is specified.

## Additional metric standoffs

The same three connection types and 6, 8, 10, 12, 15, 20, 25 and 30 mm body depths are available for M2.5, M4, M5 and M6. Decimal sizes use the bolt catalogue convention in IDs/navigation (`m2_5`) and decimal display labels (`M2.5`).

| Size | Pitch (mm) | Across flats (mm) | Stud length, each (mm) | Nominal blind cavity depth (mm) |
| --- | ---: | ---: | ---: | ---: |
| M2.5 | 0.45 | 5 | 8 | 6 |
| M4 | 0.7 | 7 | 6 | 6.5 |
| M5 | 0.8 | 10 | 8 | 10 |
| M6 | 1 | 10 | 10 | 10 |

Vital Parts supplies the natural-nylon M2.5 and M5 body/stud examples, RS PRO supplies the M4 example, and HStronic supplies the polyamide M6 example. Pencom independently documents the metric pitches. These are one chosen body/stud series per nominal size, not a claim that other suppliers use the same dimensions. The shared depth range and two-stud versions are catalogue extensions; availability has not been established for every combination.

As with M3, the tapped-to-tapped model is through-tapped. For stud-to-tapped, actual model cavity depth is the lesser of the table value and body depth minus 1 mm. The cavity has a flat floor; usable thread engagement, drill-point shape, tolerances and runout are not certified supplier geometry. Stud length is additional to body depth. Full meshes use the declared nominal diameter and pitch for both internal and external helical threads.

## Reference implementation

The staged population, canonical records, README sections, taxonomy navigation and A4 header/view/summary layout follow `oomp_hardware_bolt_version_5`. Its Blender studio modules (`hardware_model_render.py`, `hardware_model_blender.py`, `hardware_model_pose.py`) were copied locally from commit `579e4fe20b197dc501669f77a2bb3c4fe687ffaa`, so rendering does not depend on the sibling checkout. Those inherited modules retain their upstream coding style; this catalogue's declarations use explicit assignments and function-top defaults.
