import networkx as nx

from graph_pipeline import build_graph, draw_graph, compute_layout

G = nx.Graph()

progress_percents = build_graph(G=G)

pos = compute_layout(G)
draw_graph(G=G, pos=pos, progress_percents=progress_percents)
