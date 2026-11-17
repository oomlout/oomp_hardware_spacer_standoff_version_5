"""Generate dimensioned SVG/PDF/PNG sheets from canonical OOMP records."""
from working_spacer_drawing import drawing_svg


def main(**kwargs):
    return make_svg(**kwargs)


def make_svg(**kwargs):
    import working_spacer_drawing
    return working_spacer_drawing.main(**kwargs)

if __name__ == "__main__":
    main()
