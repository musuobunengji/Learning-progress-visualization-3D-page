# ChapterGraph

**Document Relationship Analysis Pipeline (Python)**

ChapterGraph is a Python-based data processing pipeline that analyzes relationships between chapters across multiple technical documents.
It converts semi-structured technical content into structured data, extracts semantic signals, builds an inverted index, and generates chapter-to-chapter relationship edges based on shared features.

This project focuses on **internal engineering tooling**, **data pipelines**, and **information retrieval fundamentals**, and is designed to be extensible toward semantic embeddings and visualization.

---

## ✨ Key Features

* **Rule-based document ingestion**
  Convert curated technical documents into structured JSON representations.

* **Semantic signal extraction**
  Extract meaningful textual signals (e.g. keywords) at the chapter level.

* **Inverted index construction**
  Build a keyword → chapter lookup table for efficient candidate generation.

* **Relationship edge generation**
  Generate chapter-to-chapter edges using shared feature overlap and scoring.

* **Modular pipeline design**
  Each stage (ingestion, enrichment, indexing, edge generation) is isolated and reusable.

---

## 🧱 Pipeline Overview

```
Raw Content (TXT)
      ↓
Ingestion
      ↓
Structured JSON
      ↓
Signal Enrichment
      ↓
Keyword Index (Inverted Index)
      ↓
Candidate Generation
      ↓
Edge Scoring
      ↓
Chapter Relationship Graph
```

This follows a **classical multi-stage retrieval pipeline**:

* Fast pruning via inverted index
* Lightweight scoring based on feature overlap
* Designed for future semantic re-ranking (embeddings, vector search)

---

## 📁 Project Structure

```
.
├── book_content/
│   ├── books.yaml                 # Book configuration (metadata & paths)
│   ├── core_java_content.txt
│   ├── spring_in_action_content.txt
│   └── spring_start_here_content.txt
│
├── feature_achievement/
│   ├── ingestion.py               # Document ingestion & parsing
│   ├── enrichment.py              # Signal / keyword extraction
│   ├── index.py                   # Inverted index construction
│   ├── edge_generation.py         # Candidate generation & scoring
│   ├── pipeline.py                # End-to-end pipeline entry
│   └── __init__.py
│
└── README.md
```

---

## ▶️ How to Run

> ⚠️ **Note**
> This project assumes the input documents are **curated technical texts**.
> The ingestion logic is intentionally conservative and does not aim to handle arbitrary raw files.

### 1. Configure input documents

Edit `book_content/books.yaml`:

```yaml
books:
  - book_name: core-java
    content_path: book_content/core_java_content.txt

  - book_name: spring-in-action
    content_path: book_content/spring_in_action_content.txt
```

---

### 2. Run the pipeline

From the project root:

```bash
python -m feature_achievement.pipeline
```

This will:

1. Load all configured documents
2. Enrich chapters with semantic signals
3. Build a keyword inverted index
4. Generate chapter-to-chapter relationship edges

The resulting edges are printed to stdout (or can be redirected to JSON).

---

## 🔗 Edge Format (Example)

```json
{
  "from": "core-java::ch3",
  "to": "spring-in-action::ch1",
  "type": "keyword_overlap",
  "score": 4
}
```

* `from` / `to`: Chapter IDs
* `type`: Relationship type
* `score`: Number of shared keywords (lightweight similarity signal)

---

## 🧠 Design Decisions

* **Rule-based first**
  Feature extraction is intentionally rule-based to ensure transparency and debuggability.

* **Index before scoring**
  Inverted index drastically reduces comparison complexity.

* **Chapter-level granularity**
  Relationships are modeled between chapters, not entire books.

* **Pipeline > script**
  The codebase is structured as a pipeline, not a one-off analysis script.

---

## 🚀 Future Work

* Semantic embeddings for reranking (e.g. sentence transformers)
* Vector index (FAISS / HNSW)
* FastAPI service layer
* Message-queue–based batch processing
* Graph visualization frontend

---

## 🛠 Tech Stack

* Python 3
* Standard library (argparse, dataclasses, typing)
* YAML-based configuration
* Modular pipeline architecture

---

## 📌 Status

This project is actively evolving and currently focuses on:

* Data ingestion correctness
* Pipeline clarity
* Retrieval & candidate generation fundamentals

