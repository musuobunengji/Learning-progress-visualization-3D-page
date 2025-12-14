import json
from pathlib import Path

BASE_DIR = Path(__file__).parent
DEFAULT_DATA_PATH = BASE_DIR / "data.json"


def load_nodes(path: Path = DEFAULT_DATA_PATH):
    """load nodes data"""
    nodes = json.loads(path.read_text())["nodes"]
    return nodes


def load_edges(path: Path = DEFAULT_DATA_PATH):
    """load edges data"""
    edges = json.loads(path.read_text())["edges"]
    return edges
