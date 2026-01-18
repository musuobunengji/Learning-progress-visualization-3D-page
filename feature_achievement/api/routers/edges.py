from typing import List

from fastapi import APIRouter, Depends
from sqlmodel import select, Session

from feature_achievement.api.deps import (
    get_retrieval_pipline,
    get_enriched_books,
)
from feature_achievement.db.engine import get_session
from feature_achievement.db.models import Edge, Chapter
from feature_achievement.db.crud import persist_edges, persist_books_and_chapters
from feature_achievement.retrieval.edge_generation import generate_edges

router = APIRouter(prefix="", tags=["edges"])


@router.post("/compute-edges")
def compute_edges(
    session: Session = Depends(get_session),
    pipeline=Depends(get_retrieval_pipline),
    enriched_books=Depends(get_enriched_books),
):
    """
    Run retrieval pipeline and persist edges into database.
    Return edges count.
    """
    edges = generate_edges(enriched_books, pipeline)
    persist_books_and_chapters(enriched_books, session)
    persist_edges(edges, session)

    return {
        "count": len(edges),
        "message": "edges computed and stored successfully",
    }


@router.get("/edges")
def list_edges(
    book_id: str,
    session: Session = Depends(get_session),
):
    """Query edges by book_id (from_chapter belongs to the book)."""
    stmt = (
        select(Edge)
        .join(Chapter, Edge.from_chapter == Chapter.id)
        .where(Chapter.book_id == book_id)
    )
    # stmt = select(Edge).where(
    #     or_(
    #         Edge.from_chapter.like(f"{book_id}%"),
    #         Edge.to_chapter.like(f"{book_id}%"),
    #     )
    # )

    edges = session.exec(stmt).all()
    return {
        "count": len(edges),
        "edges": edges,
    }
