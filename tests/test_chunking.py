
from src.chunking import chunk_text


def test_chunk_text_returns_chunks():
    text = (
        "Employees receive 25 days of annual leave per year.\n\n"
        "Employees must request leave at least 7 days before "
        "the planned leave date.\n\n"
        "Managers are responsible for approving or rejecting "
        "leave requests.\n\n"
        "Emergency leave can be requested without the 7-day "
        "notice requirement."
    )

    chunks = chunk_text(text)

    assert len(chunks) >= 1
    assert all(isinstance(chunk, str) for chunk in chunks)
    assert all(chunk.strip() for chunk in chunks)
