"""Declare parts here; working_oomp makes the canonical records."""
import copy
import fnmatch
import yaml
from catalogue_io import ROOT
from oomp_populate_helper import build_oomp_id, write_extras
from working_oomp_populate_spacer import generate as generate_spacer
from working_oomp_populate_standoff import generate as generate_standoff
from working_spacer_definitions import add_definitions


def main(**kwargs):
    part_filter = kwargs.get("filter", "*") or "*"
    options = []
    options.extend(generate_spacer())
    options.extend(generate_standoff())
    manual = yaml.safe_load((ROOT / "working_manual.yaml").read_text(encoding="utf-8")) or {}
    for entry in manual.get("options", []):
        family = entry.get("type_name")
        if family not in ("spacer", "standoff"):
            raise ValueError("Manual type_name must be spacer or standoff")
        depth = float(entry["depth_mm"])
        if depth <= 0:
            raise ValueError("Manual depth_mm must be positive")
        generate = generate_spacer if family == "spacer" else generate_standoff
        generate_kwargs = {}
        generate_kwargs["depths"] = [depth]
        generate_kwargs["nominal_sizes"] = [entry.get("nominal_size", "m3").lower()]
        if entry.get("connection_type"):
            generate_kwargs["connection_types"] = [entry["connection_type"]]
        options.extend(generate(**generate_kwargs))
    extras = []
    seen = set()
    for option in options:
        extra = copy.deepcopy(option)
        part_id = build_oomp_id(extra)
        if part_id in seen or not fnmatch.fnmatchcase(part_id, part_filter):
            continue
        seen.add(part_id)
        add_definitions(part=extra)
        extras.append(extra)
    import working_oomp_populate_extra_detail
    working_oomp_populate_extra_detail.main(extras=extras)
    write_extras(extras)
    return extras


if __name__ == "__main__":
    main()
