
import pytest
from pydantic import ValidationError

from src.ingestion.models import CanonicalDocument, DocumentBlock


def test_valid_document():
    block = DocumentBlock(
        block_id="block-1",
        block_type="paragraph",
        text="Emergency leave does not require seven days' notice.",
        order=0,
        page_number=3,
        section_path=["Leave Policy", "Emergency Leave"],
    )

    document = CanonicalDocument(
        document_id="company-policy",
        source="data/raw/company_policy.pdf",
        file_type="pdf",
        content_hash="example-sha256",
        version="v1",
        blocks=[block],
    )

    assert document.blocks[0].page_number == 3
    assert document.blocks[0].section_path == [
        "Leave Policy",
        "Emergency Leave",
    ]
    assert document.warnings == []


def test_invalid_page_number_is_rejected():
    with pytest.raises(ValidationError):
        DocumentBlock(
            block_id="block-1",
            block_type="paragraph",
            text="Policy text",
            order=0,
            page_number=0,
        )


def test_document_requires_at_least_one_block():
    with pytest.raises(ValidationError):
        CanonicalDocument(
            document_id="company-policy",
            source="data/raw/company_policy.txt",
            file_type="txt",
            content_hash="example-sha256",
            version="v1",
            blocks=[],
        )
