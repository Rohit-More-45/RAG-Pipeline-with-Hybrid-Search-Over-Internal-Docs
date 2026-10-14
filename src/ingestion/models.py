
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class DocumentBlock(BaseModel):
    """One ordered content block extracted from a source document."""

    model_config = ConfigDict(extra="forbid")

    block_id: str = Field(min_length=1)
    block_type: Literal[
        "heading",
        "paragraph",
        "list",
        "table",
        "code",
        "other",
    ]
    text: str
    order: int = Field(ge=0)

    page_number: int | None = Field(default=None, ge=1)
    section_path: list[str] = Field(default_factory=list)

    start_offset: int | None = Field(default=None, ge=0)
    end_offset: int | None = Field(default=None, ge=0)


class CanonicalDocument(BaseModel):
    """Normalized document shared by all format-specific loaders."""

    model_config = ConfigDict(extra="forbid")

    document_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    file_type: Literal["pdf", "txt", "md", "docx"]

    content_hash: str = Field(min_length=1)
    version: str = Field(min_length=1)

    blocks: list[DocumentBlock] = Field(min_length=1)
    warnings: list[str] = Field(default_factory=list)
