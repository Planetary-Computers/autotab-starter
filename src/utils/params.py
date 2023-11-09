import json
import os
from typing import Optional

params = None


def load(filepath: Optional[str] = None):
    global params
    if filepath is None or not os.path.exists(filepath):
        return
    with open(filepath) as f:
        params = json.load(f)


def get(key: str):
    global params
    if params is None:
        raise Exception("Params not loaded")
    return params[key]
