"""Shared file helpers; importing this module never generates assets."""
from pathlib import Path
import fnmatch
import yaml

ROOT = Path(__file__).resolve().parent


def records(**kwargs):
    directory = Path(kwargs.get("directory", ROOT / "parts"))
    part_filter = kwargs.get("filter", "*") or "*"
    result = []
    for path in sorted(directory.glob("*/working.yaml")):
        if fnmatch.fnmatchcase(path.parent.name, part_filter):
            part = yaml.safe_load(path.read_text(encoding="utf-8"))
            result.append((path.parent, part))
    return result


def write_text(**kwargs):
    path = Path(kwargs["path"])
    text = kwargs["text"]
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding="utf-8") == text:
        return
    path.write_text(text, encoding="utf-8", newline="\n")


def write_yaml(**kwargs):
    path = kwargs["path"]
    data = kwargs["data"]
    write_text(path=path, text=yaml.safe_dump(data, sort_keys=False, allow_unicode=True))
