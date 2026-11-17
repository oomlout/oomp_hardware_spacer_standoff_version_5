"""Publish deterministic catalogue pages after asset generation."""

def main(**kwargs):
    import working_readme
    return working_readme.main(**kwargs)


if __name__ == "__main__":
    main()
