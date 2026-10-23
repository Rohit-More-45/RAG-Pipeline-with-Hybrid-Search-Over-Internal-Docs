
import pytest

from src.ingestion.models import CanonicalDocument, DocumentBlock
from src.ingestion.validation import validate_canonical_document


def make_document(blocks):
    return CanonicalDocument(
        document_id="policy",
        source="data/raw/policy.txt",
        file_type="txt",
        content_hash="abc123",
        version="v1",
        blocks=blocks,
    )


def make_block(block_id, order, text="Annual leave policy"):
    return DocumentBlock(
        block_id=block_id,
        block_type="paragraph",
        text=text,
        order=order,
    )


def test_valid_document_passes():
    document = make_document([
        make_block("block-0", 0, "Employees receive annual leave."),
        make_block("block-1", 1, "Managers approve leave requests."),
    ])

    validate_canonical_document(document)


def test_duplicate_block_ids_are_rejected():
    document = make_document([
        make_block("duplicate", 0),
        make_block("duplicate", 1),
    ])

    with pytest.raises(ValueError, match="IDs must be unique"):
        validate_canonical_document(document)


def test_non_contiguous_block_order_is_rejected():
    document = make_document([
        make_block("block-0", 0),
        make_block("block-2", 2),
    ])

    with pytest.raises(ValueError, match="contiguous"):
        validate_canonical_document(document)


def test_blank_block_text_is_rejected():
    document = make_document([
        make_block("block-0", 0, "   "),
    ])

    with pytest.raises(ValueError, match="no meaningful text"):
        validate_canonical_document(document)
