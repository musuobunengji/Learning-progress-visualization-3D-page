from fastapi import APIRouter, Depends

from feature_achievement.api.deps import get_enriched_books, get_retrieval_pipline
from feature_achievement.retrieval.edge_generation import generate_edges

router = APIRouter(prefix="/edges", tags=["edges"])


@router.get("")
def get_edges(
    pipeline=Depends(get_retrieval_pipline), enriched_books=Depends(get_enriched_books)
):
    edges = generate_edges(enriched_books, pipeline)
    return {
        "count": len(edges),
        "edges": edges,
    }
