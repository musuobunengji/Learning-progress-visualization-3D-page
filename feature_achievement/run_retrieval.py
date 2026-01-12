from feature_achievement.enrichment import load_all_enriched_data

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


def main():
    # 1️⃣ load enriched data（和以前一模一样）
    enriched_books = load_all_enriched_data("book_content/books.yaml")

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
        min_score=0.1,
    )

    # 7️⃣ run edge generation（真正的“跑图”）
    edges = generate_edges(enriched_books, retrieval_pipeline)

    print(len(edges))
    print(edges[:10])  # 只打前几个看看


if __name__ == "__main__":
    main()
