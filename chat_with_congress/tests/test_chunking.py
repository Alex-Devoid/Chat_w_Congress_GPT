"""
Unit tests for chunking service.
"""

from chat_with_congress.app.api.services.chunking import chunk_text

def test_chunking():
    text = "This is a sample text that should be chunked into smaller pieces."
    chunks = chunk_text(text, max_chunk_size=20)
    assert len(chunks) == 4, "Chunking failed"
