import matplotlib.pyplot as plt
import networkx as nx


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
