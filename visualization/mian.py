import networkx as nx
from pathlib import Path
import argparse
from visualization.graph_pipeline import build_graph, draw_graph, compute_layout
from visualization.graph_pipeline import ValidationError
import traceback


def main():
    parser = argparse.ArgumentParser(description="Graph visualization tool")
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to input JSON file(default:data.json)",
    )
    args = parser.parse_args()

    G = nx.Graph()

    try:
        if args.input:
            progress_percents = build_graph(G, args.input)
        else:
            progress_percents = build_graph(G)
    except FileNotFoundError:
        print("Please enter vaild path!")
    except ValidationError as e:
        print(f"[Validation Error] {e}")
    except Exception:
        traceback.print_exc()
    else:
        pos = compute_layout(G)
        draw_graph(G=G, pos=pos, progress_percents=progress_percents)


if __name__ == "__main__":
    main()
