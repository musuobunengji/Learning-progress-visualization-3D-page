def build_keyword_index(enriched_books):
    index = {}  # keyword -> set(chapter_id)
    for book in enriched_books:
        for chapter in book["chapters"]:
            keywords = (
                chapter.get("signals", {}).get("features", {}).get("keywords", [])
            )
            # print(keywords)
            for kw in keywords:
                index.setdefault(kw, set()).add(chapter["id"])

    return index
