from pydantic import BaseModel
from typing import Optional


class ComputeEdgesRequest(BaseModel):
    book_ids: list[str]
    enrichment_version: str = "v1_bullets+sections"

    candidate_generator: str = "tfidf_token"
    similarity: str = "tfidf"

    min_score: float = 0.1
