#!/bin/bash

# Create necessary directories if they don't exist
echo "Setting up directory structure..."
mkdir -p chat_with_congress/app/api/endpoints
mkdir -p chat_with_congress/app/api/models
mkdir -p chat_with_congress/app/api/services
mkdir -p chat_with_congress/tests

# Create or update chunking.py
echo "Creating chunking service..."
cat <<EOL > chat_with_congress/app/api/services/chunking.py
"""
chunking.py

This module contains logic to split long text responses into smaller,
context-preserving chunks that can be processed more effectively.
"""

def chunk_text(text, max_chunk_size=1000):
    """
    Splits the input text into smaller chunks, each with a maximum size.

    :param text: The input text to be chunked.
    :param max_chunk_size: The maximum size of each chunk.
    :return: A list of text chunks.
    """
    words = text.split()
    chunks = []
    chunk = []

    for word in words:
        if len(' '.join(chunk)) + len(word) + 1 <= max_chunk_size:
            chunk.append(word)
        else:
            chunks.append(' '.join(chunk))
            chunk = [word]
    
    if chunk:
        chunks.append(' '.join(chunk))
    
    return chunks
EOL

# Create or update semantic_search.py
echo "Creating semantic search service..."
cat <<EOL > chat_with_congress/app/api/services/semantic_search.py
"""
semantic_search.py

This module contains logic to perform semantic search on text chunks,
retrieving and ranking the most relevant information based on a query.
"""

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def semantic_search(query, chunks):
    """
    Performs a semantic search on the given chunks of text.

    :param query: The search query string.
    :param chunks: The list of text chunks to search within.
    :return: The most relevant chunk.
    """
    vectorizer = TfidfVectorizer().fit_transform([query] + chunks)
    vectors = vectorizer.toarray()

    cosine_matrix = cosine_similarity(vectors[0:1], vectors[1:])
    relevance_scores = cosine_matrix[0]
    
    most_relevant_idx = relevance_scores.argmax()
    return chunks[most_relevant_idx], relevance_scores[most_relevant_idx]
EOL

# Create or update members.py
echo "Creating endpoint logic for members..."
cat <<EOL > chat_with_congress/app/api/endpoints/members.py
"""
members.py

This module handles API requests related to Congress members, including
searching for members, retrieving details, and performing chats.
"""

from fastapi import APIRouter, HTTPException
from chat_with_congress.app.api.models.requests import (
    MemberSearchRequest, MemberDetailsRequest, ChatRequest
)
from chat_with_congress.app.api.services.chunking import chunk_text
from chat_with_congress.app.api.services.semantic_search import semantic_search
import requests
import os

router = APIRouter()
API_KEY = os.getenv("CONGRESS_GOV_API_KEY")
BASE_URL = "https://api.congress.gov/v3"

@router.post("/search-members/", summary="Search for members of Congress")
def search_members(request: MemberSearchRequest):
    """
    Search for members of Congress by name.
    Returns a list of members matching the search criteria.
    """
    response = requests.get(f"{BASE_URL}/member", params={"query": request.name, "api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@router.post("/member-details/", summary="Get details of a member of Congress")
def get_member_details(request: MemberDetailsRequest):
    """
    Get detailed information about a specific member of Congress by ID.
    Returns the member's details including name, bio, and roles.
    """
    response = requests.get(f"{BASE_URL}/member/{request.member_id}", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@router.post("/chat/", summary="Chat about a member of Congress")
def chat(request: ChatRequest):
    """
    Chat about a member of Congress using their ID.
    Responds to questions about the specified member.
    """
    # Fetch member details
    response = requests.get(f"{BASE_URL}/member/{request.member_id}", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    
    member_details = response.json()
    # Convert member details to a long text
    member_text = f"Details of {member_details['name']}:\n{member_details['bio']}\n{member_details['roles']}"
    
    # Chunk the text
    chunks = chunk_text(member_text)
    
    # Perform semantic search
    relevant_chunk, score = semantic_search(request.question, chunks)
    
    return {"response": relevant_chunk, "score": score}
EOL

# Update main.py to include the new router
echo "Updating main.py to include the new router..."
cat <<EOL > chat_with_congress/app/api/main.py
from fastapi import FastAPI
from chat_with_congress.app.api.endpoints import members

app = FastAPI(
    title="Chat with Congress",
    description="This API allows users to chat with data pulled from the Congress.gov API.",
    version="1.0.0",
    servers=[
        {
            "url": "http://localhost:8000",
            "description": "Local server"
        }
    ]
)

# Include routers
app.include_router(members.router)
EOL

# Create or update unit tests in the tests directory
echo "Creating unit tests..."
cat <<EOL > chat_with_congress/tests/test_chunking.py
"""
Unit tests for chunking service.
"""

from chat_with_congress.app.api.services.chunking import chunk_text

def test_chunking():
    text = "This is a sample text that should be chunked into smaller pieces."
    chunks = chunk_text(text, max_chunk_size=20)
    assert len(chunks) == 4, "Chunking failed"
EOL

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
EOL

echo "Project setup complete!"
