# Catalogue maintenance

- Follow the user's verbose dictionary style: one field assignment per line, multiline editable lists, `**kwargs`, and defaults at the beginning of each routine.
- Declare parts in `working_oomp_populate_*.py`; make canonical records in `working_oomp.py`; generate drawings through `working_svg.py`, SCAD through `working_scad.py`, and studio assets through `working_three_d_model.py`.
- Use `stud` for external threads and `tapped` for internal threads. Connection variants are `tapped_to_tapped`, `stud_to_tapped`, and `stud_to_stud`. Keep body depth separate from stud and overall lengths.
- Keep exactly one populated round-spacer OD series per nominal screw size. Record the supplier evidence for diameter choices.
- Keep `hardware / family / nominal size / variant and material / dimensions / depth` navigation. Sort dimensions numerically.
- Follow the bolt catalogue's Summary, Details, Parts, Assembly README structure and its restrained drawing/studio presentation.
- Preserve explicit source limitations. Never label an assumed through thread as a verified supplier tapping depth.
- Run the relevant tests, `working_validate.py`, and inspect drawing/render previews before claiming completion.
- The user's preferred online name is Martin McDoozle. Do not infer a name from filesystem paths.
