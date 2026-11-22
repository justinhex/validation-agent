import sys
import json
import pytest

from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent/"src")
)

from validation_agent.helpers.input_loader import load_inputs


def test_load_inputs_from_files(tmp_path):
    req_rel_path = "requirements/REQ-001.md"
    req_file = tmp_path / "requirements" / "REQ-001.md"
    req_file.parent.mkdir(parents = True, exist_ok = True)
    req_file.write_text(
        "## REQ-001: test requirement. \n",
        encoding = "utf-8"
    )

    header_rel_path = "dut/include/window_api.h"
    header_file = tmp_path / "dut" / "include" / "window_api.h"
    header_file.parent.mkdir(parents = True, exist_ok = True)
    header_file.write_text(
        "#pragma once \n",
        encoding = "utf-8"
    )

    planner_json = json.dumps(
        {
            "files":[req_rel_path, header_rel_path]
        }
    )

    pack_root = str(tmp_path)

    output = load_inputs(
        planner_json=planner_json,
        pack_root=pack_root
    )

    assert not output == {}, (
        f"{output} cannot be empty!"
    )

    assert output[req_rel_path] == "## REQ-001: test requirement. \n"
    assert output[header_rel_path] == "#pragma once \n"

def test_load_inputs_outside_pack_root(tmp_path):
    planner_json = json.dumps(
        {
            "files":["../outside.txt"]
        }
    )

    pack_root = str(tmp_path)

    with pytest.raises(ValueError): 
        load_inputs(
            planner_json=planner_json,
            pack_root=pack_root
        )

def test_file_not_found(tmp_path):
    planner_json = json.dumps(
        {
            "files":["requirments/REQ-001.md","dut/include/window_api.h"]
        }
    )

    pack_root = str(tmp_path)

    with pytest.raises(FileNotFoundError):
        load_inputs(
            planner_json=planner_json,
            pack_root=pack_root
        )

def test_input_not_dict(tmp_path):
    planner_json = json.dumps(
        ["/requirments/REQ-001.md","/dut/include/window_api.h"]
    )

    pack_root = str(tmp_path)

    with pytest.raises(ValueError):
        load_inputs(
            planner_json=planner_json,
            pack_root=pack_root
        )

def test_input_no_files(tmp_path):
    planner_json = json.dumps(
        {
            "file":["/requirments/REQ-001.md","/dut/include/window_api.h"]
        }
    )

    pack_root = str(tmp_path)

    with pytest.raises(ValueError):
        load_inputs(
            planner_json=planner_json,
            pack_root=pack_root
        )

def test_input_not_list(tmp_path):
    planner_json = json.dumps(
        {
            "files": '"/requirments/REQ-001.md","/dut/include/window_api.h"'
        }
    )

    pack_root = str(tmp_path)

    with pytest.raises(ValueError):
        load_inputs(
            planner_json=planner_json,
            pack_root=pack_root
        )

def test_input_empty_list(tmp_path):
    planner_json = json.dumps(
        {
            "files": []
        }
    )

    pack_root = str(tmp_path)

    with pytest.raises(ValueError):
        load_inputs(
            planner_json=planner_json,
            pack_root=pack_root
        )

def test_not_json_file(tmp_path):
    planner_json = "{not Json"
        

    pack_root = str(tmp_path)

    with pytest.raises(ValueError):
        load_inputs(
            planner_json=planner_json,
            pack_root=pack_root
        )
        





    