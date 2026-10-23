
from src.ingestion.models import CanonicalDocument


def validate_canonical_document(
    document: CanonicalDocument,
) -> None:
    """Raise ValueError if a canonical document is inconsistent."""

    if not document.source.strip():
        raise ValueError("Document source must not be empty")

    if not document.content_hash.strip():
        raise ValueError("Document content hash must not be empty")

    if not document.blocks:
        raise ValueError("Document must contain at least one block")

    block_ids = [block.block_id for block in document.blocks]

    if len(block_ids) != len(set(block_ids)):
        raise ValueError("Document block IDs must be unique")

    orders = [block.order for block in document.blocks]

    if sorted(orders) != list(range(len(document.blocks))):
        raise ValueError(
            "Block order values must be unique and contiguous from zero"
        )

    for block in document.blocks:
        if not block.text.strip():
            raise ValueError(
                f"Block {block.block_id!r} contains no meaningful text"
            )

        if (
            block.start_offset is not None
            and block.end_offset is not None
            and block.end_offset < block.start_offset
        ):
            raise ValueError(
                f"Block {block.block_id!r} has invalid character offsets"
            )
