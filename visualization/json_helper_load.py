import json


def load_nodes(path):
    """load nodes data"""
    nodes = json.loads(path.read_text())["nodes"]
    return nodes


def load_edges(path):
    """load edges data"""
    edges = json.loads(path.read_text())["edges"]
    return edges
