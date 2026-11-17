"""Make canonical OOMP records from the declarations in parts_source."""
import copy
from pathlib import Path
import oomp
from oomp_populate_helper import build_oomp_id
from catalogue_io import ROOT, records, write_yaml


def main(**kwargs):
    return load_parts(**kwargs)


def load_parts(**kwargs):
    make_files = kwargs.get("make_files", True)
    part_filter = kwargs.get("filter", "*") or "*"
    source_directory = kwargs.get("source_directory", ROOT / "parts_source")
    output_directory = Path(kwargs.get("output_directory", ROOT / "parts"))
    parts = []

    for source_folder, source in records(directory=source_directory, filter=part_filter):
        details = copy.deepcopy(source)
        part_id = build_oomp_id(details)
        if part_id != source_folder.name:
            raise ValueError(f"Source folder does not match taxonomy: {source_folder}")
        part = oomp.add_part(make_files=False, **details)
        part.pop("make_files", None)
        part["name"] = part_id
        part["name_space"] = part_id.replace("_", " ")
        part["name_proper"] = part["name_space"].title()
        part["directory"] = f"parts/{part_id}"
        part["link_github"] = f"https://github.com/oomlout/oomp_hardware_spacer_standoff_version_5/tree/main/parts/{part_id}"
        part["link_main"] = part["link_github"]
        part["link_redirect"] = part["link_github"]
        if make_files:
            write_yaml(path=output_directory / part_id / "working.yaml", data=part)
        parts.append(part)
    return parts


def create_generic(**kwargs):
    return load_parts(**kwargs)


if __name__ == "__main__":
    main()
