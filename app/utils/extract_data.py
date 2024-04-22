import json
from pathlib import Path

def extract_data(path: Path) -> float:
    with open(path) as user_file:
        file_contents = user_file.read()
    parsed_json = json.loads(file_contents)
    return parsed_json['totals']