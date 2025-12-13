import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()

# 节点
G.add_node("lpv-3D")
G.add_node("FastAPI")
G.add_node("Python")
G.add_node("NumPy")
G.add_node("matplotlib")
G.add_node("networkx")
# 关系
G.add_edge("FastAPI", "Python")
G.add_edge("FastAPI", "lpv-3D")
G.add_edge("Python", "lpv-3D")
G.add_edge("Python", "NumPy")
G.add_edge("Python", "matplotlib")
G.add_edge("Python", "networkx")

# 画图
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_size=1200)
plt.show()
