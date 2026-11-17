"""Rebuild this part from the editable adjacent parameters.json."""
import json
from pathlib import Path
import sys

folder = Path(__file__).resolve().parent
sys.path.insert(0, str(folder.parents[2]))
from working_three_d_model import generate_assets

if __name__ == "__main__":
    recipe = json.loads((folder / "parameters.json").read_text(encoding="utf-8"))
    generate_assets(part={"three_d_model": recipe}, folder=folder.parent, force=True)
