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

from json_helper_load import load_nodes, load_edges
from normalize_progress import normalize_progress


def build_graph(G):
    nodes = load_nodes()
    edges = load_edges()

    # add nodes
    progress_percents = []
    for node in nodes:
        if validate_node(node_data=node):
            progress_percent = node["content"]["progress_percentage"]
            progress_percents.append(normalize_progress(progress_percent))
            G.add_node(node["id"], progress_percent=progress_percent)

    # add edges
    for edge in edges:
        if validate_edge(edge_data=edge, nodes=nodes):
            G.add_edge(edge["from"], edge["to"])

    return progress_percents


def validate_node(node_data):
    """
    validate: the id of one node exists and the progress_percentage for
      content in one node exists;
      return True/False
    """
    if (
        node_data["id"] is not None
        and node_data["content"]["progress_percentage"] is not None
    ):
        return True
    else:
        return False


def validate_edge(edge_data, nodes):
    """
    validate: the from and to for the edge must in note;
    return True/False
    """
    node_ids = {node["id"] for node in nodes}
    if edge_data["from"] in node_ids and edge_data["to"] in node_ids:
        return True
    else:
        return False


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
