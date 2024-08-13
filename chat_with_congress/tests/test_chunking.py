"""
Unit tests for chunking service.
"""

from app.api.services.chunking import chunk_text

import tiktoken  # Assuming the use of OpenAI's tiktoken library for token counting


def calculate_tokens(text):
    encoding = tiktoken.get_encoding("gpt-3.5-turbo")
    return len(encoding.encode(text))


def test_chunking():
    text = "This is a sample text that should be chunked into smaller pieces."
    chunks = chunk_text(text, max_chunk_size=20)
    assert len(chunks) == 4, "Chunking failed"
    for chunk in chunks:
        assert calculate_tokens(chunk) < 4096  # Example token limit

def test_chunking_edge_case():
    text = "Short text."
    chunks = chunk_text(text, max_chunk_size=20)
    assert len(chunks) == 1, "Chunking failed on short text"
    assert chunks[0] == "Short text.", "Chunking failed to return the correct chunk"
    assert calculate_tokens(chunks[0]) < 4096  # Example token limit
