import json
from pathlib import Path

class FileHandler:
    """Thin wrapper around reading/writing JSON blobs inside the data folder."""
    def __init__(self, filename):
        self.path = Path("data") / filename
        self.path.parent.mkdir(exist_ok=True)

        if not self.path.exists():
            self.write([])

    def read(self):
        """Return the JSON contents as Python data structures."""
        with open(self.path, "r") as f:
            return json.load(f)

    def write(self, data):
        """Serialize the provided data back to JSON with indentation."""
        with open(self.path, "w") as f:
            json.dump(data, f, indent=4)
