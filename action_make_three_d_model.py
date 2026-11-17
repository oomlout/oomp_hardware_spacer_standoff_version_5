"""Rebuild models/renders from canonical records, then refresh the pages."""

def main(**kwargs):
    import working_three_d_model
    import working_readme
    working_three_d_model.main(**kwargs)
    working_readme.main()


if __name__ == "__main__":
    main()
