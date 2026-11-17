"""Optional per-ID notes; edit this file to add source-specific details."""
from oomp_populate_helper import build_oomp_id


def main(**kwargs):
    extras = kwargs.get("extras", [])
    extras_dict = {}
    for extra in extras:
        extras_dict[build_oomp_id(extra)] = extra

    # Example: add a note without changing the geometric declaration.
    # part_id = "hardware_spacer_m3_nylon_white_7_mm_outer_diameter_10_mm_depth"
    # if part_id in extras_dict:
    #     extras_dict[part_id]["notes"] = "Your manually maintained note."
