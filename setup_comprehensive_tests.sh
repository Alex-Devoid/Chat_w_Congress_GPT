#!/bin/bash

# Create or update tests for the members endpoints and other related endpoints
echo "Creating unit tests for all endpoints..."
cat <<EOL > chat_with_congress/tests/test_endpoints.py
"""
Unit tests for all endpoints.
"""

from fastapi.testclient import TestClient
from chat_with_congress.app.api.main import app
from unittest.mock import patch
import tiktoken  # Assuming the use of OpenAI's tiktoken library for token counting

client = TestClient(app)

def calculate_tokens(text):
    encoding = tiktoken.get_encoding("gpt-3.5-turbo")
    return len(encoding.encode(text))

def test_search_members():
    with patch("chat_with_congress.app.api.endpoints.members.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"results": [{"name": "John Doe"}]}
        response = client.post("/search-members/", json={"name": "John Doe"})
        assert response.status_code == 200
        assert response.json() == {"results": [{"name": "John Doe"}]}
        assert calculate_tokens(response.json()) < 4096  # Example token limit

        mock_get.return_value.status_code = 500
        response = client.post("/search-members/", json={"name": "Jane Doe"})
        assert response.status_code == 500
        assert response.json() == {"detail": "Error fetching data from Congress.gov API"}

def test_get_member_details():
    with patch("chat_with_congress.app.api.endpoints.members.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "John Doe", "bio": "A bio", "roles": ["role1", "role2"]}
        response = client.post("/member-details/", json={"member_id": "A000360"})
        assert response.status_code == 200
        assert response.json() == {"name": "John Doe", "bio": "A bio", "roles": ["role1", "role2"]}
        assert calculate_tokens(response.json()) < 4096  # Example token limit

        mock_get.return_value.status_code = 404
        response = client.post("/member-details/", json={"member_id": "A000360"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Error fetching data from Congress.gov API"}

def test_chat():
    with patch("chat_with_congress.app.api.endpoints.members.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"name": "John Doe", "bio": "A bio", "roles": ["role1", "role2"]}
        
        response = client.post("/chat/", json={"question": "Tell me about the roles", "member_id": "A000360"})
        assert response.status_code == 200
        assert "response" in response.json()
        assert "score" in response.json()
        assert calculate_tokens(response.json()) < 4096  # Example token limit

        mock_get.return_value.status_code = 404
        response = client.post("/chat/", json={"question": "Tell me about the roles", "member_id": "A000360"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Error fetching data from Congress.gov API"}

# Repeat similar tests for all other endpoints: transcripts, bill-details, etc.
EOL

# Create or update tests for chunking service including token size
echo "Creating unit tests for chunking service with token size consideration..."
cat <<EOL > chat_with_congress/tests/test_chunking.py
"""
Unit tests for chunking service.
"""

from chat_with_congress.app.api.services.chunking import chunk_text
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
EOL

# Create or update tests for semantic search service
echo "Creating unit tests for semantic search service..."
cat <<EOL > chat_with_congress/tests/test_semantic_search.py
"""
Unit tests for semantic search service.
"""

from chat_with_congress.app.api.services.semantic_search import semantic_search

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
    assert score == 0.0, "Semantic search should return 0.0 score when no match"
EOL

# Output final message
echo "Comprehensive unit tests created successfully!"
