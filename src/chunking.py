
import hashlib

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(
    text: str,
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> list[str]:
    """Split text into overlapping chunks."""

    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")

    if not 0 <= chunk_overlap < chunk_size:
        raise ValueError(
            "chunk_overlap must be >= 0 and smaller than chunk_size"
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
    )

    return splitter.split_text(text)


def chunk_document(
    document: dict,
    chunk_size: int = 300,
    chunk_overlap: int = 50,
) -> list[dict]:
    """Split a loaded document while preserving its metadata."""

    text = document["text"]
    document_metadata = document["metadata"]

    if not isinstance(text, str):
        raise TypeError("Document text must be a string")

    if not text.strip():
        return []

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""],
        add_start_index=True,
    )

    split_documents = splitter.create_documents(
        texts=[text],
        metadatas=[document_metadata],
    )

    chunks = []

    for index, split_document in enumerate(split_documents):
        chunk_text_content = split_document.page_content
        metadata = {
            **split_document.metadata,
            "chunk_index": index,
            "start_index": split_document.metadata.get("start_index", -1),
            "char_count": len(chunk_text_content),
        }

        id_source = (
            f"{document_metadata['document_id']}:"
            f"{index}:{chunk_text_content}"
        )
        chunk_id = hashlib.sha256(
            id_source.encode("utf-8")
        ).hexdigest()[:16]

        chunks.append(
            {
                "id": chunk_id,
                "text": chunk_text_content,
                "metadata": metadata,
            }
        )

    return chunks
