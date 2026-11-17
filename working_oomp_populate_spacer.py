"""Manually editable M3-M6 clearance spacers. Dimensions are millimetres."""
import copy


def series_definitions(**kwargs):
    series = {}

    m3 = {}
    m3["bore_mm"] = 3.2
    m3["outer_diameter_mm"] = 7
    m3["depths"] = [
        3,
        5,
        6,
        8,
        10,
        12,
        15,
    ]
    m3["source_refs"] = [
        "soundtronics_spacers",
        "siqma_spacer_10",
        "vxb_spacer_depths",
    ]
    series["m3"] = m3

    m4 = {}
    m4["bore_mm"] = 4.3
    m4["outer_diameter_mm"] = 7
    m4["depths"] = [
        3,
        5,
        6,
        8,
        10,
        12,
        15,
        20,
        25,
        30,
    ]
    m4["source_refs"] = [
        "user_spacer_od_selection",
        "pencom_spacer_bores_depths",
    ]
    series["m4"] = m4

    m5 = {}
    m5["bore_mm"] = 5.3
    m5["outer_diameter_mm"] = 9
    m5["depths"] = [
        3,
        5,
        6,
        8,
        10,
        12,
        15,
        20,
        25,
        30,
    ]
    m5["source_refs"] = [
        "user_spacer_od_selection",
        "pencom_spacer_bores_depths",
    ]
    series["m5"] = m5

    m6 = {}
    m6["bore_mm"] = 6.4
    m6["outer_diameter_mm"] = 11
    m6["depths"] = [
        3,
        5,
        6,
        8,
        10,
        12,
        15,
        20,
        25,
        30,
    ]
    m6["source_refs"] = [
        "user_spacer_od_selection",
        "pencom_spacer_bores_depths",
    ]
    series["m6"] = m6
    return series


def generate(**kwargs):
    nominal_sizes = kwargs.get("nominal_sizes", [
        "m3",
        "m4",
        "m5",
        "m6",
    ])
    depths = kwargs.get("depths", None)
    bore_mm = kwargs.get("bore_mm", None)
    outer_diameter_mm = kwargs.get("outer_diameter_mm", None)
    series = series_definitions()
    options = []

    for nominal_size in nominal_sizes:
        if nominal_size not in series:
            raise ValueError("Spacer nominal size must be m3, m4, m5 or m6")
        dimensions = series[nominal_size]
        selected_depths = depths if depths is not None else dimensions["depths"]
        selected_bore = bore_mm if bore_mm is not None else dimensions["bore_mm"]
        selected_od = outer_diameter_mm if outer_diameter_mm is not None else dimensions["outer_diameter_mm"]
        for depth in selected_depths:
            option = {}
            option["taxonomy_1"] = "hardware"
            option["taxonomy_2"] = "spacer"
            option["taxonomy_3"] = nominal_size
            option["taxonomy_4"] = "nylon_white"
            option["taxonomy_5"] = f"{selected_od:g}_mm_outer_diameter"
            option["taxonomy_6"] = f"{depth:g}_mm_depth"
            option["shape"] = "round"
            option["material"] = "nylon"
            option["colour"] = "white"
            option["nominal_size"] = nominal_size
            option["bore_mm"] = selected_bore
            option["outer_diameter_mm"] = selected_od
            option["depth_mm"] = depth
            option["threaded"] = False
            option["dimension_status"] = "Generic catalogue dimensions; not a manufacturer-specific drawing."
            option["dimension_note"] = f"{nominal_size.upper()} denotes screw compatibility; the plain clearance bore is {selected_bore:g} mm, not a thread."
            if nominal_size != "m3":
                option["dimension_note"] += " Outside diameter follows the user-specified catalogue series; supplier references support bore and depth choices only."
            option["source_refs"] = copy.deepcopy(dimensions["source_refs"])
            options.append(copy.deepcopy(option))
    return options
