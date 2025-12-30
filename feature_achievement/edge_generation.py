def generate_edges(enriched_books, keyword_index):
    edges = []
    chapter_keywords = build_chapter_keyword_map(enriched_books)

    for book in enriched_books:
        for chapter in book["chapters"]:
            src_id = chapter["id"]
            keywords = (
                chapter.get("signals", {}).get("features", {}).get("keywords", [])
            )

            candidates = set()
            for kw in keywords:
                candidates |= keyword_index.get(kw, set())

            candidates.discard(src_id)

            keywords_A = chapter_keywords[src_id]
            for tgt_id in candidates:
                keywords_B = chapter_keywords[tgt_id]
                score = len(keywords_A & keywords_B)
                edges.append(
                    {
                        "from": src_id,
                        "to": tgt_id,
                        "type": "keyword_overlap",
                        "score": score,
                    }
                )

    return edges


def build_chapter_keyword_map(enriched_books):
    """chapter_id -> set(keywords)"""
    chapter_keywords = {}

    for book in enriched_books:
        for chapter in book["chapters"]:
            chapter_id = chapter["id"]
            keywords = (
                chapter.get("signals", {}).get("features", {}).get("keywords", [])
            )
            chapter_keywords[chapter_id] = set(keywords)

    return chapter_keywords
