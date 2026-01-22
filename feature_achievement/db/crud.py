from feature_achievement.db.models import Book, Chapter, Edge, Run


def persist_books_and_chapters(enriched_books, session):
    """
    Persist books and chapters into database.
    Assumes enriched_books structure:
    {
        "book_id": str,
        "chapters": [...]
    }
    """

    for book in enriched_books:
        book_id = book["book_id"]
        chapters = book["chapters"]
        existing = session.get(Book, book_id)
        if not existing:
            # 1️⃣ persist Book
            session.add(Book(id=book_id, title=book_id, size=len(chapters)))

        # 2️⃣ persist Chapters
        for ch in book["chapters"]:
            if not session.get(Chapter, ch["id"]):
                session.add(
                    Chapter(
                        id=ch["id"],
                        book_id=book_id,
                        title=ch.get("title"),
                        chapter_text=ch["chapter_text"],
                    )
                )

    session.commit()


def persist_edges(edges, run_id: int, session):
    for e in edges:
        session.add(
            Edge(
                run_id=run_id,
                from_chapter=e["from"],
                to_chapter=e["to"],
                score=e["score"],
                type=e["type"],
            )
        )
    session.commit()
