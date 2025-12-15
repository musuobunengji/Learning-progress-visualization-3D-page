import networkx as nx
import matplotlib.pyplot as plt

from json_helper_load import load_nodes, load_edges
from validate_data import validate_node, validate_edge
from normalize_progress import normalize_progress
from draw_graph import draw_graph
from compute_layout import compute_layout

G = nx.Graph()

nodes = load_nodes()
edges = load_edges()

# 节点
progress_percents = []
for node in nodes:
    if validate_node(node_data=node):
        progress_percent = node["content"]["progress_percentage"]
        progress_percents.append(normalize_progress(progress_percent))
        G.add_node(node["id"], progress_percent=progress_percent)

# 关系
for edge in edges:
    if validate_edge(edge_data=edge, nodes=nodes):
        G.add_edge(edge["from"], edge["to"])

# 画图
pos = compute_layout(G)
draw_graph(G, pos=pos, progress_percents=progress_percents)
