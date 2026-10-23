
import hashlib
from pathlib import Path

from src.ingestion.models import CanonicalDocument, DocumentBlock
from src.ingestion.validation import validate_canonical_document


def load_txt_document(
    file_path: str | Path,
    version: str = "v1",
) -> CanonicalDocument:
    """Load a UTF-8 text file into the canonical document structure."""

    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Document not found: {path}")

    raw_bytes = path.read_bytes()
    text = raw_bytes.decode("utf-8")
    content_hash = hashlib.sha256(raw_bytes).hexdigest()

    text = text.replace("\r\n", "\n").replace("\r", "\n").strip()

    if not text:
        raise ValueError(f"Document contains no text: {path}")

    paragraphs = [
        paragraph.strip()
        for paragraph in text.split("\n\n")
        if paragraph.strip()
    ]

    blocks = []
    search_from = 0

    for order, paragraph in enumerate(paragraphs):
        start_offset = text.find(paragraph, search_from)
        end_offset = start_offset + len(paragraph)
        search_from = end_offset

        blocks.append(
            DocumentBlock(
                block_id=f"{path.stem}-block-{order:04d}",
                block_type="paragraph",
                text=paragraph,
                order=order,
                start_offset=start_offset,
                end_offset=end_offset,
            )
        )

        document = CanonicalDocument(
        document_id=path.stem,
        source=str(path.resolve()),
        file_type="txt",
        content_hash=content_hash,
        version=version,
        blocks=blocks,
    )

    validate_canonical_document(document)

    return document

