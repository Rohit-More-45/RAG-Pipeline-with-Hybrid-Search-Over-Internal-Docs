
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ChunkingConfig(BaseModel):
    """Validated settings for document chunking experiments."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    child_chunk_size: int = Field(default=500, ge=1)
    child_chunk_overlap: int = Field(default=60, ge=0)
    parent_chunk_size: int = Field(default=1500, ge=1)
    chunking_version: str = Field(default="v1", min_length=1)

    @model_validator(mode="after")
    def validate_chunk_sizes(self):
        if self.child_chunk_overlap >= self.child_chunk_size:
            raise ValueError(
                "Child overlap must be smaller than child chunk size"
            )

        if self.parent_chunk_size < self.child_chunk_size:
            raise ValueError(
                "Parent chunk size must be at least the child chunk size"
            )

        return self
