# ChapterGraph

**Retrieval-Oriented Chapter Relationship Analysis Pipeline (Python)**

ChapterGraph is a Python-based retrieval pipeline that analyzes relationships between chapters across multiple curated technical documents.

The project focuses on **turning semi-structured technical content into structured signals**, and on **designing a debuggable, multi-stage retrieval workflow** for discovering cross-document relationships.
Rather than optimizing for maximum semantic power, the system emphasizes **pipeline clarity, controllable complexity, and engineering realism**.

This repository is designed as an **internal engineering tool prototype**, with a clear evolution path toward embeddings, vector search, and service deployment.

---

## ✨ Core Capabilities

* **Deterministic document ingestion**
  Convert curated technical texts into a normalized, chapter-centric JSON schema.

* **Signal enrichment at chapter granularity**
  Aggregate chapter-level textual signals (sections, bullets) into a canonical representation used consistently across the pipeline.

* **Multi-stage retrieval workflow**
  Explicit separation between candidate generation and similarity scoring, following classical information retrieval design.

* **Inverted-index–based candidate pruning**
  Use lightweight lexical signals to aggressively reduce the comparison space before scoring.

* **Continuous similarity scoring**
  Apply TF-IDF–based similarity to produce interpretable, continuous relevance scores instead of binary overlaps.

* **Modular, extensible architecture**
  Candidate generation, similarity scoring, and pipeline orchestration are abstracted to allow controlled evolution.

---

## 🧱 Pipeline Overview

```
Curated Technical Text
        ↓
Ingestion
        ↓
Structured Chapter JSON
        ↓
Signal Enrichment
        ↓
Chapter Text Normalization
        ↓
Candidate Generation (Inverted Index)
        ↓
Similarity Scoring (TF-IDF)
        ↓
Chapter Relationship Graph
```

The system follows a **classical multi-stage retrieval funnel**:

* **Early pruning for efficiency** (candidate generation)
* **Scoring for relevance** (similarity computation)
* **Designed for future semantic upgrades**, without coupling them prematurely to the core pipeline

---

## 📁 Project Structure

```
.
├── book_content/
│   ├── books.yaml                 # Document configuration
│   ├── core_java_content.txt
│   ├── spring_in_action_content.txt
│   └── spring_start_here_content.txt
│
├── feature_achievement/
│   ├── ingestion/                 # Parsing & normalization
│   ├── enrichment/                # Chapter-level signal construction
│   │
│   ├── retrieval/
│   │   ├── candidates/            # Candidate generation strategies
│   │   ├── similarity/            # Similarity scoring strategies
│   │   ├── utils/                 # Shared builders (TF-IDF, indices)
│   │   ├── pipeline.py            # RetrievalPipeline orchestration
│   │   └── edge_generation.py     # Thin edge construction layer
│   │
│   └── __init__.py
│
└── README.md
```

The codebase is structured to clearly distinguish between:

* **Workflow orchestration**
* **Replaceable retrieval strategies**
* **Shared resource construction**

---

## ▶️ Running the Pipeline

> ⚠️ **Assumption**
> Input documents are **manually curated technical texts**.
> Ingestion is intentionally conservative and not designed for arbitrary raw files.

### 1. Configure documents

Edit `book_content/books.yaml`:

```yaml
- book_name: core-java
  content_path: book_content/core_java_content.txt

- book_name: spring-in-action
  content_path: book_content/spring_in_action_content.txt
```

---

### 2. Execute retrieval pipeline

From the project root:

```bash
python -m feature_achievement.run_retrieval
```

This will:

1. Load and normalize all configured documents
2. Construct chapter-level text signals
3. Build inverted indices for candidate generation
4. Compute TF-IDF similarity scores
5. Generate chapter-to-chapter relationship edges

Edges are printed to stdout and can be redirected or persisted as needed.

---

## 🔗 Edge Format

```json
{
  "from": "core-java::ch3",
  "to": "spring-in-action::ch1",
  "type": "tfidf_similarity",
  "score": 0.37
}
```

* `from` / `to`: Chapter identifiers
* `type`: Relationship type
* `score`: Continuous similarity score (TF-IDF)

---

## 🧠 Design Rationale

* **Pipeline before models**
  The system prioritizes observability and debuggability over early use of opaque models.

* **Candidate generation ≠ similarity scoring**
  Retrieval stages are explicitly separated to control complexity and scaling behavior.

* **Stop at the right abstraction boundary**
  Embeddings and vector databases are recognized as the natural next step, but intentionally excluded to keep the project realistic, inspectable, and aligned with intern-level ownership.

* **Interfaces over hard-coded logic**
  Core components are abstracted to enable future extensions without structural rewrites.

---

## 🚀 Intended Extensions (Out of Scope for Current Version)

* Embedding-based similarity (sentence transformers)
* Vector indices (FAISS / HNSW)
* FastAPI service layer for internal tooling
* Batch processing via message queues
* Graph visualization frontend

These are treated as **future evolution paths**, not missing features.

---

## 🛠 Tech Stack

* Python 3
* scikit-learn (TF-IDF)
* YAML-based configuration
* Modular, retrieval-oriented pipeline design

---

## 📌 Project Status

This project intentionally concludes at a **retrieval-focused, pre-embedding stage** and currently emphasizes:

* Correctness of ingestion and normalization
* Clear separation of retrieval stages
* Stable and explainable system behavior
* Sound engineering judgment over feature breadth