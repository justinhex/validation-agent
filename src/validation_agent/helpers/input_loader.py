import json

from pathlib import Path


def load_inputs(
        planner_json : str, pack_root : str
    ) -> dict[str, str]:

    output_data = {}

    try:
        data = json.loads(planner_json)

    except json.JSONDecodeError:
        raise ValueError("Planner JSON is malformed!")

    if not isinstance(data, dict):
        raise ValueError("Planner JSON must be a dict!")

    if "files" not in data:
        raise ValueError("Cannot find files!")

    elif not isinstance(data["files"], list):
        raise ValueError("Files must be a list!")

    elif data["files"] == []:
        raise ValueError("Empty files list!")

    for file_path in data["files"]:
        abs_path = Path(pack_root) / file_path
        if not Path(abs_path).resolve().is_relative_to(pack_root):
            raise ValueError(f"{file_path} is not under {pack_root}!")
        
        try:
            with open(abs_path, encoding="utf-8") as target_file:
                    output_data[file_path] = target_file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f'{file_path} is NOT found!')

    return output_data

