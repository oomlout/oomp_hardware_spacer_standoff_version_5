"""The catalogue pipeline: declare, make records, draw/model, document."""
import copy


def main(**kwargs):
    kwargs["run_oomp_populate"] = kwargs.get("run_oomp_populate", True)
    kwargs["run_oomp"] = kwargs.get("run_oomp", True)
    kwargs["run_scad"] = kwargs.get("run_scad", True)
    kwargs["run_svg"] = kwargs.get("run_svg", True)
    kwargs["run_three_d_model"] = kwargs.get("run_three_d_model", True)
    kwargs["run_action"] = kwargs.get("run_action", True)
    kwargs["run_solidcraft"] = kwargs.get("run_solidcraft", False)
    kwargs["generate_stl"] = kwargs.get("generate_stl", False)
    kwargs["export_stl"] = kwargs.get("export_stl", True)
    kwargs["render"] = kwargs.get("render", True)
    return run(**kwargs)


def run(**kwargs):
    run_oomp_populate = kwargs.get("run_oomp_populate", False)
    run_oomp = kwargs.get("run_oomp", False)
    run_scad = kwargs.get("run_scad", False)
    run_svg = kwargs.get("run_svg", False)
    run_three_d_model = kwargs.get("run_three_d_model", False)
    run_action = kwargs.get("run_action", False)
    run_solidcraft = kwargs.get("run_solidcraft", False)
    generate_stl = kwargs.get("generate_stl", False)
    export_stl = kwargs.get("export_stl", True)
    export_extras = kwargs.get("export_extras", False)
    verify_solidcraft = kwargs.get("verify_solidcraft", False)
    native_context = copy.deepcopy(kwargs.get("solidcraft_context") or {})
    import working_cad
    selected_solidcraft = working_cad.solidcraft_mode(run_solidcraft)
    if selected_solidcraft == "working_scad":
        native_context["recipe_source"] = "working_scad"
    native_context["export_stl"] = export_stl
    native_context["export_extras"] = export_extras
    native_context["verify_solidcraft"] = verify_solidcraft
    options = copy.deepcopy(kwargs)
    for key in [
        "run_oomp_populate", "run_oomp", "run_scad", "run_svg", "run_three_d_model",
        "run_action", "run_solidcraft", "solidcraft_context", "generate_stl",
        "export_stl", "export_extras", "verify_solidcraft",
    ]:
        options.pop(key, None)
    if run_oomp_populate:
        import working_oomp_populate
        working_oomp_populate.main(**options)
    if run_oomp:
        import working_oomp
        working_oomp.main(**options)
    if run_scad:
        import working_scad
        working_scad.main(generate_stl=generate_stl, **options)
    if run_svg:
        import working_svg
        working_svg.main(**options)
    if run_solidcraft:
        import working_solidcraft
        working_solidcraft.main(solidcraft_context=native_context)
    if run_three_d_model:
        import working_three_d_model
        working_three_d_model.main(export_stl=export_stl, **options)
    if run_action:
        import working_action
        working_action.main(**options)


if __name__ == "__main__":
    main()
