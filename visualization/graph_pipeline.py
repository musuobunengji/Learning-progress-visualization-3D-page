"""
data → graph → layout → visualization-ready
------------------------------
build_graph()
↓
validate_graph() ok
↓
compute_layout() ok
↓
draw_graph() ok
------------------------------
"""

import matplotlib.pyplot as plt
import networkx as nx
from pathlib import Path

from visualization.json_helper_load import load_nodes, load_edges
from visualization.normalize_progress import normalize_progress

BASE_DIR = Path(__file__).parent
DEFAULT_DATA_PATH = BASE_DIR / "data.json"


class ValidationError(Exception):
    """Raised when input data fails validation"""


def build_graph(G, path: Path = DEFAULT_DATA_PATH):
    nodes = load_nodes(path)
    edges = load_edges(path)

    # add nodes
    progress_percents = []
    for node in nodes:
        if validate_node(node_data=node):
            progress_percent = node["content"]["progress_percentage"]
            progress_percents.append(normalize_progress(progress_percent))
            G.add_node(node["id"], progress_percent=progress_percent)

    # add edges
    node_ids = {node["id"] for node in nodes}
    for edge in edges:
        if validate_edge(edge_data=edge, node_ids=node_ids):
            G.add_edge(edge["from"], edge["to"])

    return progress_percents


def validate_node(node_data):
    """ """
    # 1. Check ID
    if node_data.get("id") == "":
        raise ValidationError("NodeIdIsEmpty")
    elif node_data.get("id") is None:
        raise ValidationError("NodeIdIsNone")

    # 2. Get the percentage value safely
    percentage_raw = node_data.get("content", {}).get("progress_percentage")

    # 3. Check if empty
    if percentage_raw == "":
        raise ValidationError("NodeProgressPercentageIsEmpty")

    # 4. Attempt to validate if it is a number
    # Add range checks (e.g., must be 0-100)
    try:
        # float() handles both integers like "10" and floats like "10.5"
        # It also catches non-numeric strings like "abc"
        numeric_value = float(percentage_raw)
    except TypeError:
        # Triggered if it's not a number (e.g. "abc") or is None
        raise ValidationError("NodeProgressPercentageIsNotANumber")
    else:
        if not (0 <= numeric_value <= 100):
            raise ValidationError("NodeProgressPercentageOutOfRange")

    # All checks passed
    return True


def validate_edge(edge_data, node_ids):
    """
    validate: the from and to for the edge must in note;
    """
    if edge_data.get("from") not in node_ids:
        raise ValidationError("EdgeFromNotValue")
    elif edge_data.get("to") not in node_ids:
        raise ValidationError("EdgeToNotValue")
    else:
        return True


def compute_layout(G):
    pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42, scale=20, center=(0, 0))
    return pos


def draw_graph(G, pos, progress_percents):
    """drawing logic"""
    fig, ax = plt.subplots()
    ax.set_aspect("equal")

    nx.draw(
        G,
        pos,
        ax=ax,
        node_color=progress_percents,
        cmap=plt.cm.Blues,
        with_labels=True,
        node_size=1200,
    )

    sm = plt.cm.ScalarMappable(
        cmap=plt.cm.Blues,
        norm=plt.Normalize(vmin=min(progress_percents), vmax=max(progress_percents)),
    )
    sm.set_array([])

    plt.colorbar(sm, ax=ax)
    plt.show()
