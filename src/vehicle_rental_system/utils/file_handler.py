import json
from pathlib import Path

class FileHandler:
    def __init__(self, filename):
        self.path = Path("data") / filename
        self.path.parent.mkdir(exist_ok=True)

        if not self.path.exists():
            self.write([])

    def read(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def write(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
