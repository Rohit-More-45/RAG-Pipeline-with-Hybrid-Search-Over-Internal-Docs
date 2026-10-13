
from pathlib import Path

import pytest

from src.document_loader import load_text_document


def test_load_text_document_returns_text_and_metadata(tmp_path):
    file_path = tmp_path / "policy.txt"
    file_path.write_text(
        "Employees receive 25 days of annual leave.",
        encoding="utf-8",
    )

    result = load_text_document(file_path)

    assert result["text"] == "Employees receive 25 days of annual leave."
    assert result["status"] == "completed"
    assert result["warnings"] == []
    assert result["metadata"]["document_id"] == "policy"
    assert result["metadata"]["file_type"] == "txt"
    assert result["metadata"]["char_count"] == len(result["text"])
    assert result["metadata"]["content_hash"]


def test_empty_file_produces_warning(tmp_path):
    file_path = tmp_path / "empty.txt"
    file_path.write_text("", encoding="utf-8")

    result = load_text_document(file_path)

    assert result["text"] == ""
    assert result["status"] == "completed_with_warnings"
    assert result["warnings"]


def test_missing_file_raises_error(tmp_path):
    file_path = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        load_text_document(file_path)


def test_line_endings_are_normalized(tmp_path):
    file_path = tmp_path / "lines.txt"
    file_path.write_bytes(b"First line\r\nSecond line\rThird line")

    result = load_text_document(file_path)

    assert result["text"] == "First line\nSecond line\nThird line"
