from functools import lru_cache

from feature_achievement.enrichment import load_all_enriched_data
from feature_achievement.retrieval.utils.text import collect_chapter_texts
from feature_achievement.retrieval.utils.tfidf import (
    build_tfidf_index,
    extract_top_tfidf_tokens,
    build_token_index,
)
from feature_achievement.retrieval.candidates.tfidf_token import (
    TfidfTokenCandidateGenerator,
)
from feature_achievement.retrieval.similarity.tfidf import TfidfSimilarityScorer
from feature_achievement.retrieval.pipeline import RetrievalPipeline


@lru_cache
def get_retrieval_pipline() -> RetrievalPipeline:
    """
    Build retrieval pipline once and reuse it.
    """
    enriched_books = load_all_enriched_data("book_content/books.yaml")

    chapter_texts = collect_chapter_texts(enriched_books)
    tfidf_index = build_tfidf_index(chapter_texts)

    chapter_top_tokens = extract_top_tfidf_tokens(tfidf_index, top_n=20)
    token_index = build_token_index(chapter_top_tokens)

    candidate_generator = TfidfTokenCandidateGenerator(
        chapter_top_tokens=chapter_top_tokens,
        token_index=token_index,
        min_shared_tokens=2,
    )

    similarity_scorer = TfidfSimilarityScorer(tfidf_index)

    return RetrievalPipeline(
        candidate_generator=candidate_generator,
        similarity_scorer=similarity_scorer,
        min_score=0.1,
    )


@lru_cache
def get_enriched_books():
    """
    Load data once.
    """
    return load_all_enriched_data("book_content/books.yaml")
