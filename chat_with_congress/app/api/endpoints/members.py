from fastapi import APIRouter, HTTPException
from chat_with_congress.app.api.models.requests import (
    MemberSearchRequest, MemberDetailsRequest, ChatRequest, MembersResponse, 
    MemberDetailsResponse, ChatResponse, BillRequest, BillActionResponse, 
    BillAmendmentResponse
)
from chat_with_congress.app.api.services.congress_api import (
    get_member_details, search_members, get_bill_details, get_bill_actions, 
    get_bill_amendments
)
from chat_with_congress.app.api.services.chunking import chunk_text
from chat_with_congress.app.api.services.semantic_search import semantic_search
import os

router = APIRouter()
API_KEY = os.getenv("CONGRESS_GOV_API_KEY")

@router.post("/search-members/", response_model=MembersResponse, summary="Search for members of Congress")
def search_members(request: MemberSearchRequest):
    """
    Search for members of Congress by name.
    Returns a list of members matching the search criteria.
    """
    return search_members(api_key=API_KEY, query=request.name)

@router.post("/member-details/", response_model=MemberDetailsResponse, summary="Get details of a member of Congress")
def get_member_details(request: MemberDetailsRequest):
    """
    Get detailed information about a specific member of Congress by ID.
    Returns the member's details including name, bio, and roles.
    """
    return get_member_details(request.member_id, API_KEY)

@router.post("/chat/", response_model=ChatResponse, summary="Chat about a member of Congress")
def chat(request: ChatRequest):
    """
    Chat about a member of Congress using their ID.
    Responds to questions about the specified member.
    """
    member_details = get_member_details(request.member_id, API_KEY)
    member_text = f"Details of {member_details['name']}:\n{member_details['bio']}\n{member_details['roles']}"
    chunks = chunk_text(member_text)
    relevant_chunk, score = semantic_search(request.question, chunks)
    return {"response": relevant_chunk, "score": score}

@router.get("/bill-details/", response_model=BillRequest, summary="Get details of a specific bill")
def bill_details(request: BillRequest):
    """
    Get detailed information about a specific bill.
    Returns details of the bill including the text, amendments, and actions.
    """
    return get_bill_details(request.congress, request.bill_type, request.bill_number, API_KEY)

@router.get("/bill-actions/", response_model=BillActionResponse, summary="Get actions related to a bill")
def bill_actions(request: BillRequest):
    """
    Get the list of actions on a specified bill.
    Returns the actions taken on the bill.
    """
    return get_bill_actions(request.congress, request.bill_type, request.bill_number, API_KEY)

@router.get("/bill-amendments/", response_model=BillAmendmentResponse, summary="Get amendments related to a bill")
def bill_amendments(request: BillRequest):
    """
    Get the list of amendments to a specified bill.
    Returns the amendments associated with the bill.
    """
    return get_bill_amendments(request.congress, request.bill_type, request.bill_number, API_KEY)
