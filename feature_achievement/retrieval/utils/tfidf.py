import numpy as np
from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer


def build_tfidf_index(chapter_texts: dict):
    """
    Input:
        chapter_texts: dict[chapter_id] -> text
    Output:
        {
            "chapter_ids": [...],
            "tfidf_matrix": scipy sparse matrix,
            "vectorizer": TfidfVectorizer
        }
    """
    chapter_ids = list(chapter_texts.keys())
    corpus = [chapter_texts[cid] or "" for cid in chapter_ids]

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        stop_words="english",
        min_df=1,  # ⚠️ debug-friendly
    )

    tfidf_matrix = vectorizer.fit_transform(corpus)

    return {
        "chapter_ids": chapter_ids,
        "tfidf_matrix": tfidf_matrix,
        "vectorizer": vectorizer,
    }


def extract_top_tfidf_tokens(tfidf_index, top_n=20):
    """
    Return:
        dict[chapter_id] -> list[str] (top tf-idf tokens)
    """
    chapter_ids = tfidf_index["chapter_ids"]
    tfidf_matrix = tfidf_index["tfidf_matrix"]
    feature_names = tfidf_index["vectorizer"].get_feature_names_out()

    chapter_top_tokens = {}

    for idx, chapter_id in enumerate(chapter_ids):
        row = tfidf_matrix[idx].toarray().ravel()
        if row.sum() == 0:
            chapter_top_tokens[chapter_id] = []
            continue

        top_indices = np.argsort(row)[-top_n:]
        tokens = [feature_names[i] for i in top_indices if row[i] > 0]

        chapter_top_tokens[chapter_id] = tokens

    return chapter_top_tokens


def build_token_index(chapter_top_tokens):
    """
    token -> set(chapter_id)
    """
    index = defaultdict(set)
    for cid, tokens in chapter_top_tokens.items():
        for t in tokens:
            index[t].add(cid)
    return index
