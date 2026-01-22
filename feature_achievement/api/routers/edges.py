from typing import List
import json

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select, Session

# from feature_achievement.api.deps import (
#     get_retrieval_pipline,
#     get_enriched_books,
# )
from feature_achievement.db.engine import get_session
from feature_achievement.db.models import Edge, Chapter, Book, Run
from feature_achievement.db.crud import persist_edges, persist_books_and_chapters
from feature_achievement.retrieval.edge_generation import generate_edges
from feature_achievement.enrichment import load_all_enriched_data
from .compute_edges_request import ComputeEdgesRequest

from feature_achievement.retrieval.candidates.tfidf_token import (
    TfidfTokenCandidateGenerator,
)
from feature_achievement.retrieval.similarity.tfidf import TfidfSimilarityScorer
from feature_achievement.retrieval.pipeline import RetrievalPipeline
from feature_achievement.retrieval.edge_generation import generate_edges

from feature_achievement.retrieval.utils.text import collect_chapter_texts

from feature_achievement.retrieval.utils.tfidf import (
    build_tfidf_index,
    extract_top_tfidf_tokens,
    build_token_index,
)

router = APIRouter(prefix="", tags=["edges"])


@router.post("/compute-edges")
def compute_edges(
    req: ComputeEdgesRequest,
    session: Session = Depends(get_session),
    # pipeline=Depends(get_retrieval_pipline),  # 2. 用 run 参数构建 RetrievalPipeline
    # enriched_books=Depends(get_enriched_books),
):
    """
    Run retrieval pipeline and persist edges into database.
    Return edges count.
    """
    # 1. insert run
    run = Run(
        book_ids=json.dumps(req.book_ids),
        enrichment_version=req.enrichment_version,
        candidate_generator=req.candidate_generator,
        similarity=req.similarity,
        min_store=req.min_score,
    )
    session.add(run)
    session.commit()
    session.refresh(run)  # 拿到 run.id???

    # 1️⃣ load enriched data（和以前一模一样)
    enriched_books = load_all_enriched_data("book_content/books.yaml")
    enriched_books = [b for b in enriched_books if b["book_id"] in req.book_ids]
    # 2️⃣ build TF-IDF index（retrieval 的公共资源）
    chapter_texts = collect_chapter_texts(enriched_books)
    tfidf_index = build_tfidf_index(chapter_texts)

    # 3️⃣ build TF-IDF token candidate resources
    chapter_top_tokens = extract_top_tfidf_tokens(tfidf_index, top_n=20)
    token_index = build_token_index(chapter_top_tokens)

    # 4️⃣ assemble candidate generator
    candidate_generator = TfidfTokenCandidateGenerator(
        chapter_top_tokens=chapter_top_tokens,
        token_index=token_index,
        min_shared_tokens=2,
    )

    # 5️⃣ assemble similarity scorer
    similarity_scorer = TfidfSimilarityScorer(tfidf_index)

    # 6️⃣ assemble retrieval pipeline
    retrieval_pipeline = RetrievalPipeline(
        candidate_generator=candidate_generator,
        similarity_scorer=similarity_scorer,
        min_score=req.min_score,
    )

    # 7️⃣ run edge generation（真正的“跑图”）
    edges = generate_edges(enriched_books, retrieval_pipeline)  # 3. compute edges
    persist_books_and_chapters(enriched_books, session)
    persist_edges(edges, run.id, session)  # 4. persist edges ??? with run_idS

    return {  # 5. return run_id
        "run_id": run.id,
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


@router.get("/graph")
def get_graph(
    run_id: int,
    session: Session = Depends(get_session),
):
    run = session.get(Run, run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")

    book_ids = json.loads(run.book_ids)

    books = session.exec(select(Book).where(Book.id.in_(book_ids))).all()
    chapters = session.exec(select(Chapter).where(Chapter.book_id.in_(book_ids))).all()
    edges = session.exec(select(Edge).where(Edge.run_id == run_id)).all()

    frontend = {
        "nodes": [],
        "edges": [],
    }

    for book in books:
        frontend["nodes"].append(
            {
                "id": book.id,
                "type": "book",
                "size": book.size,
            }
        )

    for chapter in chapters:
        frontend["nodes"].append(
            {"id": chapter.id, "type": "chapter", "book_id": chapter.book_id}
        )

    for edge in edges:
        frontend["edges"].append(
            {
                "source": edge.from_chapter,
                "target": edge.to_chapter,
                "score": edge.score,
                "type": edge.type,
            }
        )
    return frontend


@router.get("/runs")
def list_runs(session: Session = Depends(get_session)):
    runs = session.exec(select(Run).order_by(Run.created_at.desc())).all()
    return [
        {
            "id": r.id,
            "book_ids": json.loads(r.book_ids),
            "candidate_generator": r.candidate_generator,
            "similarity": r.similarity,
            "created_at": r.created_at,
        }
        for r in runs
    ]
