import json

def read_json(file_path):
    """Return list of dicts from a JSON file"""
    with open(file_path) as f:
        return json.load(f)
