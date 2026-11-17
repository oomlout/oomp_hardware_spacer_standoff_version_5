"""Build declarations, canonical records, drawings, SCAD, models and pages."""

def main(**kwargs):
    kwargs["generate_stl"] = kwargs.get("generate_stl", True)
    kwargs["export_stl"] = kwargs.get("export_stl", True)
    kwargs["run_solidcraft"] = kwargs.get("run_solidcraft", False)
    import working
    return working.main(**kwargs)


if __name__ == "__main__":
    main()
