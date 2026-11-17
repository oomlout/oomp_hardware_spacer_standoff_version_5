"""Manually editable metric hexagonal white nylon standoffs."""
import copy


def series_definitions(**kwargs):
    series = {}

    m2_5 = {}
    m2_5["nominal_size"] = "m2.5"
    m2_5["thread_nominal_diameter_mm"] = 2.5
    m2_5["thread_pitch_mm"] = 0.45
    m2_5["across_flats_mm"] = 5
    m2_5["stud_length_mm"] = 8
    m2_5["tapped_depth_mm"] = 6
    m2_5["source_refs"] = [
        "vital_standoff_m2_5_m5",
        "pencom_metric_standoff_threads",
    ]
    series["m2_5"] = m2_5

    m3 = {}
    m3["nominal_size"] = "m3"
    m3["thread_nominal_diameter_mm"] = 3
    m3["thread_pitch_mm"] = 0.5
    m3["across_flats_mm"] = 6
    m3["stud_length_mm"] = 6
    m3["tapped_depth_mm"] = 6
    series["m3"] = m3

    m4 = {}
    m4["nominal_size"] = "m4"
    m4["thread_nominal_diameter_mm"] = 4
    m4["thread_pitch_mm"] = 0.7
    m4["across_flats_mm"] = 7
    m4["stud_length_mm"] = 6
    m4["tapped_depth_mm"] = 6.5
    m4["source_refs"] = [
        "rs_standoff_m4",
        "pencom_metric_standoff_threads",
    ]
    series["m4"] = m4

    m5 = {}
    m5["nominal_size"] = "m5"
    m5["thread_nominal_diameter_mm"] = 5
    m5["thread_pitch_mm"] = 0.8
    m5["across_flats_mm"] = 10
    m5["stud_length_mm"] = 8
    m5["tapped_depth_mm"] = 10
    m5["source_refs"] = [
        "vital_standoff_m2_5_m5",
        "pencom_metric_standoff_threads",
    ]
    series["m5"] = m5

    m6 = {}
    m6["nominal_size"] = "m6"
    m6["thread_nominal_diameter_mm"] = 6
    m6["thread_pitch_mm"] = 1
    m6["across_flats_mm"] = 10
    m6["stud_length_mm"] = 10
    m6["tapped_depth_mm"] = 10
    m6["source_refs"] = [
        "hstronic_standoff_m6",
        "pencom_metric_standoff_threads",
    ]
    series["m6"] = m6
    return series


def generate(**kwargs):
    depths = kwargs.get("depths", [
        6,
        8,
        10,
        12,
        15,
        20,
        25,
        30,
    ])
    nominal_sizes = kwargs.get("nominal_sizes", [
        "m2_5",
        "m3",
        "m4",
        "m5",
        "m6",
    ])
    connection_types = kwargs.get("connection_types", [
        "tapped_to_tapped",
        "stud_to_tapped",
        "stud_to_stud",
    ])
    across_flats_override = kwargs.get("across_flats_mm", None)
    stud_length_override = kwargs.get("stud_length_mm", None)
    tapped_depth_override = kwargs.get("tapped_depth_mm", None)
    series = series_definitions()
    options = []

    for size in nominal_sizes:
        size_key = size.lower().replace(".", "_")
        if size_key not in series:
            raise ValueError("Standoff nominal size must be m2.5, m3, m4, m5 or m6")
        dimensions = series[size_key]
        nominal_size = dimensions["nominal_size"]
        diameter = dimensions["thread_nominal_diameter_mm"]
        pitch = dimensions["thread_pitch_mm"]
        thread = f"{nominal_size.upper()} x {pitch:g}"
        across_flats_mm = dimensions["across_flats_mm"] if across_flats_override is None else across_flats_override
        stud_length_mm = dimensions["stud_length_mm"] if stud_length_override is None else stud_length_override
        tapped_depth_mm = dimensions["tapped_depth_mm"] if tapped_depth_override is None else tapped_depth_override
        for connection_type in connection_types:
            if connection_type not in ("tapped_to_tapped", "stud_to_tapped", "stud_to_stud"):
                raise ValueError("Unknown standoff connection_type")
            for depth in depths:
                stud_count = connection_type.count("stud")
                option = {}
                option["taxonomy_1"] = "hardware"
                option["taxonomy_2"] = "standoff"
                option["taxonomy_3"] = size_key
                option["taxonomy_4"] = connection_type
                option["taxonomy_5"] = "hexagon"
                option["taxonomy_6"] = "nylon_white"
                option["taxonomy_7"] = f"{across_flats_mm:g}_mm_across_flats"
                if stud_count:
                    option["taxonomy_8"] = f"{stud_length_mm:g}_mm_stud_length"
                    option["taxonomy_9"] = f"{depth:g}_mm_depth"
                else:
                    option["taxonomy_8"] = f"{depth:g}_mm_depth"
                option["shape"] = "hexagon"
                option["material"] = "nylon"
                option["colour"] = "white"
                option["nominal_size"] = nominal_size
                option["connection_type"] = connection_type
                option["across_flats_mm"] = across_flats_mm
                option["depth_mm"] = depth
                option["stud_length_mm"] = stud_length_mm if stud_count else 0
                option["overall_length_mm"] = depth + stud_count * option["stud_length_mm"]
                option["threaded"] = True
                option["thread"] = thread
                option["thread_pitch_mm"] = pitch
                option["thread_nominal_diameter_mm"] = diameter
                option["thread_model"] = "through"
                option["tapped_depth_mm"] = depth
                option["dimension_status"] = "Generic catalogue dimensions; not a manufacturer-specific drawing."
                option["dimension_note"] = f"Model assumes a continuous {thread} through thread. Supplier tapping depth and blind/through construction vary."
                option["source_refs"] = [
                    "cqrobot_white_standoffs",
                    "lyntron_hex_standoffs",
                    "wurth_standoff_6",
                    "wurth_standoff_30",
                ]
                if connection_type == "stud_to_tapped":
                    option["thread_model"] = "blind"
                    option["tapped_depth_mm"] = min(tapped_depth_mm, depth - 1)
                    option["dimension_note"] = f"Model uses a {stud_length_mm:g} mm stud and a {option['tapped_depth_mm']:g} mm blind tapped cavity with a flat floor. Tapping is limited to body depth minus 1 mm to retain a solid web; this is an illustrative assumption, not verified usable engagement."
                    option["source_refs"] = [
                        "lyntron_stud_tapped",
                        "rs_stud_tapped",
                    ]
                if connection_type == "stud_to_stud":
                    option["thread_model"] = "external_only"
                    option["tapped_depth_mm"] = 0
                    option["dimension_note"] = f"Model uses two {stud_length_mm:g} mm {thread} studs and a solid hex body. The depth range is a catalogue extension; exact all-nylon supplier availability is not verified for every depth."
                    option["source_refs"] = [
                        "essentra_stud_stud",
                    ]
                if size_key != "m3":
                    option["source_refs"] = copy.deepcopy(dimensions["source_refs"])
                options.append(copy.deepcopy(option))
    return options
