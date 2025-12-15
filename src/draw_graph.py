import matplotlib.pyplot as plt
import networkx as nx


def draw_graph(G, pos, progress_percents):
    """drawing logic"""
    pos = nx.spring_layout(G)
    nx.draw(
        G,
        pos,
        node_color=progress_percents,
        cmap=plt.cm.Blues,
        with_labels=True,
        node_size=1200,
    )
    plt.show()
