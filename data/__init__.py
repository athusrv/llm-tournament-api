import json
import os
from models import Prompt

def load_prompts():
    dir = os.path.dirname(__file__)
    file = "data.json"
    path = os.path.join(dir, file)
    with open(path) as f:
        data = json.load(f)
    return [Prompt(**item) for item in data]