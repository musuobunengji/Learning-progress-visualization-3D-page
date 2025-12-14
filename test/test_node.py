import networkx as nx
from pathlib import Path
from src.data_load_to_graph import validate_node
from src.json_helper_load import load_nodes

BASE_DIR = Path(__file__).parent
TEST_NODE_PATH = BASE_DIR / "test_node.json"
# TEST_EDGE_PATH = BASE_DIR / "test_edge.json"
# TEST_MIX_PATH = BASE_DIR / "test_mix.json"
# TEST_SUCESS_PATH = BASE_DIR / "test_success.json"
G = nx.Graph()
nodes = load_nodes(path=TEST_NODE_PATH)


def test_validate_node():
    """test if function validate_node() work"""
    for node in nodes:
        if validate_node(node_data=node):
            G.add_node(node["id"])

    assert "lpv-3D" not in list(G.nodes)
