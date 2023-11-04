import json
from typing import Optional

data = None

def load(filepath: Optional[str] = None):
    global data
    if filepath is None:
        filepath = "data.json"
    with open(filepath) as f:
        data = json.load(f)

def get(key: str):
    global data
    if data is None:
        raise Exception("Data not loaded")
    return data[key]