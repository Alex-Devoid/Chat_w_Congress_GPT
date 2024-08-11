"""
members.py

This module handles API requests related to Congress members, including
searching for members, retrieving details, and performing chats.
"""

from fastapi import APIRouter, HTTPException
from chat_with_congress.app.api.models.requests import (
    MemberSearchRequest, MemberDetailsRequest, ChatRequest, MembersResponse, 
    MemberDetailsResponse, ChatResponse
)
from chat_with_congress.app.api.services.chunking import chunk_text
from chat_with_congress.app.api.services.semantic_search import semantic_search
import requests
import os

router = APIRouter()
API_KEY = os.getenv("CONGRESS_GOV_API_KEY")
BASE_URL = "https://api.congress.gov/v3"

@router.post("/search-members/", response_model=MembersResponse, summary="Search for members of Congress")
def search_members(request: MemberSearchRequest):
    """
    Search for members of Congress by name.
    Returns a list of members matching the search criteria.
    """
    response = requests.get(f"{BASE_URL}/member", params={"query": request.name, "api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@router.post("/member-details/", response_model=MemberDetailsResponse, summary="Get details of a member of Congress")
def get_member_details(request: MemberDetailsRequest):
    """
    Get detailed information about a specific member of Congress by ID.
    Returns the member's details including name, bio, and roles.
    """
    response = requests.get(f"{BASE_URL}/member/{request.member_id}", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@router.post("/chat/", response_model=ChatResponse, summary="Chat about a member of Congress")
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
