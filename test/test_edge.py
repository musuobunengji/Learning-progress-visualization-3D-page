import networkx as nx
from pathlib import Path
from src.validate_data import validate_edge
from src.json_helper_load import load_edges, load_nodes

BASE_DIR = Path(__file__).parent
TEST_EDGE_PATH = BASE_DIR / "test_edge.json"

G = nx.Graph()

nodes = load_nodes(path=TEST_EDGE_PATH)
edges = load_edges(path=TEST_EDGE_PATH)


def test_validate_edge():
    """test if function validate_edge() work"""
    for edge in edges:
        if validate_edge(edge_data=edge, nodes=nodes):
            G.add_edge(edge["from"], edge["to"])
    assert ("FastAPI", "lpv-3D") not in list(G.edges)
