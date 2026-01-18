from datetime import datetime, timezone
from typing import Optional

from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Chapter(SQLModel, table=True):
    id: str = Field(primary_key=True)
    book_id: str = Field(index=True)
    title: Optional[str] = None
    chapter_text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Edge(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    from_chapter: str = Field(index=True)
    to_chapter: str = Field(index=True)
    score: float
    type: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
