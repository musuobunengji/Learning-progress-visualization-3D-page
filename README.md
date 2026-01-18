# ChapterGraph

**A Retrieval-Backed Knowledge Graph for Technical Documents**

ChapterGraph is an end-to-end backend system that builds, persists, and queries semantic relationships between chapters across multiple technical books. The project is designed as a **modular retrieval pipeline** rather than a monolithic ML demo, with clear separation between ingestion, enrichment, candidate generation, similarity scoring, persistence, and API exposure.

This repository emphasizes **engineering correctness, observability, and extensibility** over premature modeling complexity.

---

## ✨ Core Capabilities

* **Document Ingestion**
  Parse structured book content into normalized JSON representations.

* **Signal Enrichment**
  Derive chapter-level textual signals (e.g. `chapter_text`) used as inputs to retrieval models.

* **Multi-Stage Retrieval Pipeline**

  * Candidate generation (pruning search space)
  * Similarity scoring (TF-IDF–based ranking)
  * Thresholding / filtering

* **Graph Construction**
  Generate directed, weighted edges between chapters representing semantic relatedness.

* **Persistent Storage (PostgreSQL)**
  Store books, chapters, and edges as first-class relational entities.

* **Retrieval-Backed API (FastAPI)**
  Expose compute and query endpoints backed by a real database.

---

## 🧠 Design Philosophy

### 1. Funnel-Based Retrieval (Classical IR)

The system follows a classical **funnel architecture**:

1. **Candidate Generation** – fast, coarse pruning (avoid full pairwise comparison)
2. **Similarity Scoring** – more expensive ranking (TF-IDF)
3. **Filtering** – score threshold / top-k
4. **Persistence** – store results for downstream use

This mirrors production-grade search and recommendation systems.

### 2. Interface-First, OO Design

Key components are defined via interfaces, enabling future extension without refactoring:

* Candidate generators (rule-based, TF-IDF token–based, etc.)
* Similarity scorers (TF-IDF today, embeddings tomorrow)
* Retrieval pipeline orchestrator

### 3. Deliberate Model Choice

TF-IDF is used intentionally as the **first semantic baseline**:

* Deterministic
* Debuggable
* Interpretable

Embedding-based similarity is treated as a **future drop-in replacement**, not a prerequisite.

---

## 🗂 Project Structure

```text
feature_achievement/
├── ingestion/              # Parse raw book content → structured JSON
│   └── ...
│
├── enrichment/             # Derive chapter-level signals (chapter_text, etc.)
│   └── ...
│
├── retrieval/
│   ├── candidates/         # Candidate generation strategies
│   │   ├── base.py
│   │   └── tfidf_token.py
│   │
│   ├── similarity/         # Similarity scoring strategies
│   │   ├── base.py
│   │   └── tfidf.py
│   │
│   ├── pipeline.py         # RetrievalPipeline orchestrator
│   └── edge_generation.py  # Convert retrieval output → graph edges
│
├── db/
│   ├── models.py           # Book / Chapter / Edge (SQLModel)
│   ├── db.py               # Engine, session, init_db
│   └── crud.py             # Persistence helpers
│
├── api/
│   ├── main.py             # FastAPI app
│   ├── deps.py             # Dependency wiring
│   └── routers/
│       └── edges.py        # Compute + query edges
│
├── scripts/
│   └── init_db.py          # Initialize database schema
│
└── pipeline.py             # Script-style pipeline entry (non-API)
```

---

## 🗄 Database Schema (PostgreSQL)

### Book

* `id` (PK)
* `title`
* `created_at`

### Chapter

* `id` (PK)
* `book_id` (indexed)
* `chapter_text`
* `created_at`

### Edge

* `id` (PK)
* `from_chapter` (indexed)
* `to_chapter` (indexed)
* `score`
* `type` (e.g. `tfidf`)
* `created_at`

The schema enforces a **node-before-edge** persistence model, mirroring graph system best practices.

---

## 🚀 Running the Project

### 1️⃣ Initialize Database

```bash
python -m feature_achievement.scripts.init_db
```

### 2️⃣ Start API Server

```bash
uvicorn feature_achievement.api.main:app --reload
```

Open Swagger UI:

```
http://127.0.0.1:8000/docs
```

---

## 🔌 API Endpoints

### `POST /compute-edges`

* Runs retrieval pipeline
* Persists books, chapters, and edges
* Designed for batch / MQ-style execution

### `GET /edges?book_id=...`

* Query all edges associated with a given book
* Returns both incoming and outgoing relationships

---

## 🧪 Observability & Debugging

The pipeline is intentionally designed to allow inspection at every stage:

* Raw chapter text
* TF-IDF vectors
* Top-N similar chapters
* Persisted edges

This makes semantic errors diagnosable **before** introducing black-box models.

---

## 🔮 Future Extensions

* Embedding-based similarity (drop-in replacement)
* Asynchronous retrieval jobs (MQ / worker)
* Edge pagination & filtering
* Graph visualization (D3 / WebGL)
* Vector database integration

---

## 📌 Summary

ChapterGraph is not a demo of a single model, but a **retrieval system**:

* Modular
* Inspectable
* Persisted
* API-backed

It is designed to scale in both **data volume** and **model sophistication** without architectural rewrites.
