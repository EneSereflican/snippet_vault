from sqlmodel import SQLModel, Field, Relationship
from enum import Enum
class SnippetTagLink(SQLModel, table=True):
    snippet_id: int | None = Field(default=None, foreign_key="snippet.id", primary_key=True)
    tag_id: int | None = Field(default=None, foreign_key="tag.id", primary_key=True)

class Tag(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    snippets: list["Snippet"] = Relationship(back_populates="tags", link_model=SnippetTagLink)

class Snippet(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    language: str
    body: str
    tags: list[Tag] = Relationship(back_populates="snippets", link_model=SnippetTagLink)

# Girdi/çıktı şemaları (table=True DEĞİL — bunlar API sözleşmesi):
class Language(str, Enum):
    python = "python"
    javascript = "js"
    typescript = "ts"
    c = "c"
    java = "java"
    go = "go"
    other = "other"

class SnippetCreate(SQLModel):
    title: str = Field(min_length=1, max_length=100)
    language: Language
    body: str = Field(min_length=1)
    tags: list[str] = []

class SnippetRead(SQLModel):
    id: int
    title: str
    language: str
    body: str
    tags: list[str] = []