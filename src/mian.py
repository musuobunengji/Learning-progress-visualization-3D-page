import networkx as nx
import matplotlib.pyplot as plt

from json_helper_load import load_nodes, load_edges
from data_load_to_graph import validate_node, validate_edge

G = nx.Graph()

nodes = load_nodes()
edges = load_edges()

# 节点
for node in nodes:
    if validate_node(node_data=node):
        progress_percent = node["content"]["progress_percentage"]
        G.add_node(node["id"], progress_percent=progress_percent)

# 关系

for edge in edges:
    if validate_edge(edge_data=edge, nodes=nodes):
        G.add_edge(edge["from"], edge["to"])
# 画图
print(f"nodes:{list(G.nodes)}")
print(list(G.edges))
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1200)
plt.show()
