from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: Optional[str] = None
    size: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Chapter(SQLModel, table=True):
    id: str = Field(primary_key=True)
    book_id: str = Field(index=True)
    title: Optional[str] = None
    chapter_text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Edge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    run_id: int = Field(index=True)

    from_chapter: str = Field(index=True)
    to_chapter: str = Field(index=True)
    score: float
    type: str  # tfidf / embedding / etc

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Run(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # 输入
    book_ids: str  # JSON string:["spring-in-action","spring-start-here"]
    enrichment_version: str  # e.g. "v1_bullets+sections"

    # 算法配置
    candidate_generator: str  # "tfidf_token"
    similarity: str
    min_store: float
    top_k: Optional[int] = None

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
