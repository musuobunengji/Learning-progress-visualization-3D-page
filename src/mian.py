import networkx as nx
import matplotlib.pyplot as plt

from json_helper_load import load_nodes, load_edges

G = nx.Graph()

nodes = load_nodes()
edges = load_edges()

# 节点
for node in nodes:
    progress_percent = node["content"]["progress_percentage"]
    G.add_node(node["id"], progress_percent=progress_percent)

# 关系
for edge in edges:
    G.add_edge(edge["from"], edge["to"])

# 画图
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1200)
plt.show()
