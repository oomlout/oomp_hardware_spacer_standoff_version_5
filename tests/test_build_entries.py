"""Build-entry contracts; all output backends are isolated from real assets."""
import importlib.util
from pathlib import Path
import sys
from types import SimpleNamespace
from unittest.mock import patch
import pytest

PROJECT = Path(__file__).resolve().parents[1]
BACKENDS = [
    "working_oomp_populate", "working_oomp", "working_scad", "working_svg",
    "working_solidcraft", "working_three_d_model", "working_action",
]


def load(filename):
    spec = importlib.util.spec_from_file_location("entry_test_" + filename, PROJECT / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_entry(filename, **kwargs):
    calls = []
    def record(name):
        return SimpleNamespace(main=lambda **options: calls.append((name, options)))
    modules = {name: record(name) for name in BACKENDS}
    modules["working"] = load("working.py")
    with patch.dict(sys.modules, modules):
        load(filename).main(**kwargs)
    return calls


def test_full_build_documents_after_models_and_uses_scad_by_default():
    calls = run_entry("action_make_all.py", filter="*_10_mm_depth")
    assert [name for name, _ in calls] == [name for name in BACKENDS if name != "working_solidcraft"]
    assert calls[2][1]["generate_stl"] is True
    assert calls[-2][1]["export_stl"] is True
    assert all(options["filter"] == "*_10_mm_depth" for _, options in calls)


def test_no_stl_build_disables_both_export_paths():
    calls = run_entry("action_make_all_no_stl.py", generate_stl=True, export_stl=True)
    assert calls[2][1]["generate_stl"] is False
    assert calls[-2][1]["export_stl"] is False
    assert "working_solidcraft" not in [name for name, _ in calls]


def test_explicit_stage_opt_out_is_respected():
    calls = run_entry("action_make_all.py", run_svg=False, run_three_d_model=False)
    assert "working_svg" not in [name for name, _ in calls]
    assert "working_three_d_model" not in [name for name, _ in calls]


def test_invalid_native_mode_fails_before_population():
    with pytest.raises(ValueError, match="run_solidcraft"):
        run_entry("action_make_all.py", run_solidcraft="false")


def test_native_context_is_separate_and_input_is_not_mutated():
    context = {"modes": ["true"], "part_filter": "pilot"}
    calls = run_entry("action_make_solidcraft.py", solidcraft_context=context, run_solidcraft="working_scad", verify_solidcraft=True)
    assert [name for name, _ in calls] == ["working_oomp_populate", "working_oomp", "working_solidcraft"]
    assert calls[-1][1]["solidcraft_context"] == {
        "modes": ["true"], "part_filter": "pilot", "recipe_source": "working_scad",
        "export_stl": True, "export_extras": True, "verify_solidcraft": True,
    }
    assert context == {"modes": ["true"], "part_filter": "pilot"}
    assert "solidcraft_context" not in calls[0][1]


@pytest.mark.parametrize("filename", ["action_make_scad.py", "action_make_scad_no_stl.py"])
def test_scad_actions_do_not_start_blender_or_native(filename):
    calls = run_entry(filename, run_solidcraft=True)
    assert [name for name, _ in calls] == ["working_oomp_populate", "working_oomp", "working_scad"]
