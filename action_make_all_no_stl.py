"""Build the catalogue without creating STL exports; retain existing STL files."""

def main(**kwargs):
    kwargs["generate_stl"] = False
    kwargs["export_stl"] = False
    kwargs["run_solidcraft"] = False
    import working
    return working.main(**kwargs)


if __name__ == "__main__":
    main()
