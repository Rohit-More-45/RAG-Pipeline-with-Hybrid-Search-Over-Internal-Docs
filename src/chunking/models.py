
from pydantic import BaseModel, ConfigDict, Field


class RetrievalChunk(BaseModel):
    """A searchable chunk linked to its source document."""

    model_config = ConfigDict(extra="forbid")

    chunk_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    document_version: str = Field(min_length=1)

    text: str = Field(min_length=1)

    chunk_index: int = Field(ge=0)
    chunking_version: str = Field(min_length=1)

    parent_id: str | None = None

    source_block_ids: list[str] = Field(min_length=1)
    page_numbers: list[int] = Field(default_factory=list)
    section_path: list[str] = Field(default_factory=list)

    start_offset: int | None = Field(default=None, ge=0)
    end_offset: int | None = Field(default=None, ge=0)

    token_count: int = Field(ge=1)
    char_count: int = Field(ge=1)
