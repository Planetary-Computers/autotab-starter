import json
import os
from typing import Optional

data = None


def load(filepath: Optional[str] = None):
    global data
    if filepath is None:
        filepath = "data.json"
    if not os.path.exists(filepath):
        return
    with open(filepath) as f:
        data = json.load(f)


def get(key: str):
    global data
    if data is None:
        raise Exception("Data not loaded")
    return data[key]
