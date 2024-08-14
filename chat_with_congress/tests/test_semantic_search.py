"""
Unit tests for semantic search service.
"""

from app.api.services.semantic_search import semantic_search

def test_semantic_search():
    chunks = ["This is the first chunk.", "This is the second chunk.", "This is the third chunk."]
    query = "second"
    relevant_chunk, score = semantic_search(query, chunks)
    assert relevant_chunk == "This is the second chunk.", "Semantic search failed"
    assert score > 0.5, "Semantic search relevance score too low"

def test_semantic_search_no_match():
    chunks = ["This is the first chunk.", "This is the second chunk.", "This is the third chunk."]
    query = "fourth"
    relevant_chunk, score = semantic_search(query, chunks)
    assert relevant_chunk == "", "Semantic search should return empty string when no match"
    assert score == 0.0, "Semantic search should return 0.0 score when no match"

