"""
Unit tests for chunking service.
"""

from app.api.services.chunking import chunk_text
import tiktoken

def calculate_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def test_chunking():
    text = "This is a sample text that should be chunked into smaller pieces."
    chunks = chunk_text(text, max_chunk_size=20)
    assert len(chunks) == 4, "Chunking failed"
    for chunk in chunks:
        assert calculate_tokens(chunk) < 4096, "Chunk exceeded token limit"

def test_chunking_edge_case():
    text = "Short text."
    chunks = chunk_text(text, max_chunk_size=20)
    assert len(chunks) == 1, "Chunking failed on short text"
    assert chunks[0] == "Short text.", "Chunking returned incorrect chunk"
    assert calculate_tokens(chunks[0]) < 4096, "Chunk exceeded token limit"
