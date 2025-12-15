import networkx as nx


def compute_layout(G):
    pos = nx.spring_layout(G, k=0.5, iterations=100, seed=42, scale=20, center=(0, 0))
    return pos
