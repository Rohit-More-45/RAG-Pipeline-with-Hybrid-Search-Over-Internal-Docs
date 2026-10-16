
from src.ingestion.models import CanonicalDocument
from src.ingestion.text_loader import load_txt_document


def test_txt_loader_returns_canonical_document(tmp_path):
    file_path = tmp_path / "policy.txt"
    file_path.write_text(
        "Employees receive 25 days of annual leave.\n\n"
        "Managers approve leave requests.",
        encoding="utf-8",
    )

    document = load_txt_document(file_path)

    assert isinstance(document, CanonicalDocument)
    assert document.document_id == "policy"
    assert document.file_type == "txt"
    assert len(document.blocks) == 2
    assert document.blocks[0].block_type == "paragraph"
    assert document.blocks[1].text == "Managers approve leave requests."


def test_txt_loader_rejects_empty_document(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    try:
        load_txt_document(file_path)
    except ValueError as error:
        assert "no text" in str(error)
    else:
        raise AssertionError("Expected empty document to be rejected")
