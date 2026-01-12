def collect_chapter_texts(enriched_books):
    """
    Return:
        dict[chapter_id]->chapter_text(str)
    """
    texts = {}

    for book in enriched_books:
        for chapter in book["chapters"]:
            texts[chapter["id"]] = chapter.get("chapter_text", "")
    return texts
