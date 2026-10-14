
import pytest
from pydantic import ValidationError

from src.chunking.models import RetrievalChunk


def test_valid_retrieval_chunk():
    chunk = RetrievalChunk(
        chunk_id="chunk-001",
        document_id="company-policy",
        document_version="v1",
        text="Employees receive 25 days of annual leave.",
        chunk_index=0,
        chunking_version="v1",
        source_block_ids=["block-001"],
        page_numbers=[1],
        section_path=["Leave Policy"],
        token_count=9,
        char_count=42,
    )

    assert chunk.document_id == "company-policy"
    assert chunk.source_block_ids == ["block-001"]
    assert chunk.token_count == 9


def test_empty_chunk_text_is_rejected():
    with pytest.raises(ValidationError):
        RetrievalChunk(
            chunk_id="chunk-001",
            document_id="company-policy",
            document_version="v1",
            text="",
            chunk_index=0,
            chunking_version="v1",
            source_block_ids=["block-001"],
            token_count=1,
            char_count=0,
        )


def test_negative_chunk_index_is_rejected():
    with pytest.raises(ValidationError):
        RetrievalChunk(
            chunk_id="chunk-001",
            document_id="company-policy",
            document_version="v1",
            text="Policy text",
            chunk_index=-1,
            chunking_version="v1",
            source_block_ids=["block-001"],
            token_count=2,
            char_count=11,
        )
