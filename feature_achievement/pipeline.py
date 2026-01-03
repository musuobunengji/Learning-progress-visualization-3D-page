from feature_achievement.enrichment import load_all_enriched_data
from feature_achievement.index import build_keyword_index
from feature_achievement.edge_generation import generate_edges

enriched_books = load_all_enriched_data("book_content/books.yaml")
index = build_keyword_index(enriched_books)
edges = generate_edges(enriched_books, index)
print(edges)
