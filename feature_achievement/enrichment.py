from feature_achievement.ingestion import convert_content_to_json
import yaml


def enrich_signals_with_keywords(data: dict) -> dict:

    for chapter in data["chapters"]:
        signals = chapter.get("signals", {})
        bullets = signals.get("bullets", [])

        if not bullets:
            continue

        all_text = " ".join(bullets).strip()
        if not all_text:
            continue

        keywords = extract_keywords(all_text)

        signals.setdefault("features", {})
        signals["features"]["keywords"] = keywords

    return data


STOPWORDS = {"the", "and", "of", "to", "a"}


def extract_keywords(text):
    words = text.lower().split()
    return [w for w in words if w not in STOPWORDS and len(w) > 4]


def load_enriched_data(book_name, content_path):
    base_data = convert_content_to_json(book_name, content_path)
    enriched_data = enrich_signals_with_keywords(base_data)
    return enriched_data


def load_all_enriched_data(config_path):
    with open(config_path, "r") as f:
        book_configs = yaml.safe_load(f)
    enriched_books = []

    for cfg in book_configs:
        enriched = load_enriched_data(
            book_name=cfg["book_name"], content_path=cfg["content_path"]
        )
        enriched_books.append(enriched)

    return enriched_books
