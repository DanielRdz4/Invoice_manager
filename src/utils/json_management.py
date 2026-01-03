#Generic functions to manage .json files
import json
from pathlib import Path

def create_json(data: dict, path):
    """creates .json file with cfdi information"""

    with path.open("w",encoding = "UTF-8") as f:
        json.dump(data, f, indent = 4)

def load_json(path: Path)-> dict:
    """Loads .json file information"""
    
    with path.open("r",encoding="UTF-8") as f:
        return json.load(f)
