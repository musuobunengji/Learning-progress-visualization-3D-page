import networkx as nx
from pathlib import Path
from src.data_load_to_graph import validate_edge, validate_node
from src.json_helper_load import load_edges, load_nodes

BASE_DIR = Path(__file__).parent
TEST_SUCESS_PATH = BASE_DIR / "test_sucess.json"

G = nx.Graph()

nodes = load_nodes(TEST_SUCESS_PATH)
edges = load_edges(TEST_SUCESS_PATH)


def test_validate_mix():
    for node in nodes:
        if validate_node(node_data=node):
            G.add_node(node["id"])
    for edge in edges:
        if validate_edge(edge_data=edge, nodes=nodes):
            G.add_edge(edge["from"], edge["to"])
    assert list(G.nodes) == [
        "FastAPI",
        "lpv-3D",
        "Python",
        "NumPy",
        "matplotlib",
        "networkx",
    ] and list(G.edges) == [
        ("FastAPI", "Python"),
        ("FastAPI", "lpv-3D"),
        ("lpv-3D", "Python"),
        ("Python", "NumPy"),
        ("Python", "matplotlib"),
        ("Python", "networkx"),
    ]
