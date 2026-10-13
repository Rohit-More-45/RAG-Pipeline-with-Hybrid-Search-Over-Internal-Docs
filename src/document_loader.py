
import hashlib
from pathlib import Path


def load_text_document(file_path: str | Path) -> dict:
    """Load a UTF-8 text file into a structured document record."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    # Read bytes first so the hash represents the original file.
    raw_bytes = path.read_bytes()
    content_hash = hashlib.sha256(raw_bytes).hexdigest()

    # Decode the file as UTF-8.
    text = raw_bytes.decode("utf-8")

    # Normalize line endings without removing paragraph boundaries.
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.strip()

    warnings = []

    if not text:
        warnings.append("The extracted document text is empty.")

    return {
        "text": text,
        "metadata": {
            "document_id": path.stem,
            "source": str(path.resolve()),
            "file_type": path.suffix.lower().lstrip("."),
            "extraction_method": "utf8_text_read",
            "content_hash": content_hash,
            "char_count": len(text),
        },
        "status": (
            "completed_with_warnings" if warnings else "completed"
        ),
        "warnings": warnings,
    }
