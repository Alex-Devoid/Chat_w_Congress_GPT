from fastapi.exceptions import RequestValidationError
from fastapi import APIRouter, HTTPException, Query

from fastapi.encoders import jsonable_encoder

from app.api.models.requests import (
    MemberSearchRequest, MemberDetailsRequest, ChatRequest, MembersResponse, 
    MemberDetailsResponse, ChatResponse, BillRequest, BillActionResponse, 
    BillAmendmentResponse, CommitteeRequest, CommitteeResponse, 
    CommunicationRequest, CommunicationResponse, SenateCommunicationResponse, BillRelatedResponse,
    BillCosponsorResponse, BillSummaryResponse, BillTextResponse,BillTitleResponse,BillDetailResponse
)
from app.api.services.congress_api import (
    get_member_details, search_members, get_bill_details, get_bill_actions, 
    get_bill_amendments, get_committee_details, get_house_communications, 
    get_senate_communications, get_bill_committees, get_bill_cosponsors, 
    get_bill_related_bills, get_bill_summaries, get_bill_text_versions, 
    get_bill_titles
)
from app.api.services.chunking import chunk_text
from app.api.services.semantic_search import semantic_search
from dotenv import load_dotenv
import os

load_dotenv() 

router = APIRouter()

API_KEY = os.getenv("CONGRESS_GOV_API_KEY")

@router.post("/search-members/", response_model=MembersResponse, summary="Search for members of Congress")
def search_members_post(request: MemberSearchRequest):
    """
    Search for members of Congress by name.
    Returns a list of members matching the search criteria.
    """
    response = search_members(api_key=API_KEY, query=request.name)
    return {"members": response.get('members', [])}



@router.post("/member-details/", response_model=MemberDetailsResponse, summary="Get details of a member of Congress")
def fetch_member_details(request: MemberDetailsRequest):
    """
    Get detailed information about a specific member of Congress by ID.
    Returns the member's details including name, bio, and roles.
    """
    member_search_response = search_members(api_key=API_KEY, query=request.member_id)

    members = member_search_response.get('members', [])
    if not members:
        raise HTTPException(status_code=404, detail="Member not found")

    bioguide_id = members[0]['bioguideId']
    member_details_response = get_member_details(bioguide_id, API_KEY)

    # Assuming the API response is structured like {'member': { ... }}
    member_data = member_details_response.get('member')
    if member_data is None:
        raise HTTPException(status_code=500, detail="Unexpected response format")
    print(member_data)
    return member_data





@router.post("/chat/", response_model=ChatResponse, summary="Chat about a member of Congress")
def chat(request: ChatRequest):
    """
    Chat about a member of Congress using their ID.
    Responds to questions about the specified member.
    """
    member_details_response = get_member_details(request.member_id, API_KEY)
    member_details = member_details_response['member']
    member_text = f"Details of {member_details['invertedOrderName']}:\n{member_details['honorificName']} {member_details['firstName']} {member_details['lastName']}"
    chunks = chunk_text(member_text)
    relevant_chunk, score = semantic_search(request.question, chunks)
    return {"response": relevant_chunk, "score": score}




@router.get("/bill-details/", response_model=BillDetailResponse, summary="Get details of a specific bill")
def bill_details(congress: int, bill_type: str, bill_number: int):
    """
    Get detailed information about a specific bill.
    Returns details of the bill including the text, amendments, and actions.
    """
    details = get_bill_details(congress, bill_type, bill_number, API_KEY)
    return details







@router.get("/bill-actions/", response_model=BillActionResponse, summary="Get actions related to a bill")
def bill_actions(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number.")
):
    """
    Get the list of actions on a specified bill.
    Returns the actions taken on the bill.
    """
    print(f"Received request: congress={congress}, bill_type={bill_type}, bill_number={bill_number}")
    response = get_bill_actions(congress, bill_type, bill_number, API_KEY)
    print(f"API response: {response}")
    return response




@router.get("/bill-amendments/", response_model=BillAmendmentResponse, summary="Get amendments related to a bill")
def bill_amendments(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hres, sres)."),
    bill_number: int = Query(..., description="The bill number.")
):
    """
    Get the list of amendments to a specified bill.
    Returns the amendments associated with the bill.
    """
    print("Received request for bill amendments")
    amendments = get_bill_amendments(congress, bill_type, bill_number, API_KEY)
    print("Amendments:", amendments)
    return amendments


@router.get("/bill-cosponsors/", response_model=BillCosponsorResponse, summary="Get cosponsors of a bill")
def bill_cosponsors(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hres, sres)."),
    bill_number: int = Query(..., description="The bill number.")
):
    """
    Get the list of cosponsors of a specific bill.
    """
    return get_bill_cosponsors(congress, bill_type, bill_number, API_KEY)


@router.get("/bill-committees/", response_model=CommitteeResponse, summary="Get committees related to a bill")
def bill_committees(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number.")
):
    """
    Get the list of committees associated with a specific bill.
    """
    return get_bill_committees(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-related-bills/", response_model=BillRelatedResponse, summary="Get related bills")
def bill_related_bills(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number.")
):
    """
    Get the list of bills related to a specific bill.
    """
    return get_bill_related_bills(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-summaries/", response_model=BillSummaryResponse, summary="Get bill summaries")
def bill_summaries(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number.")
):
    """
    Get summaries of a specific bill.
    """
    return get_bill_summaries(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-text-versions/", response_model=BillTextResponse, summary="Get bill text versions")
def bill_text_versions(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number.")
):
    """
    Get different text versions of a specific bill.
    """
    return get_bill_text_versions(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-titles/", response_model=BillTitleResponse, summary="Get bill titles")
def bill_titles(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number.")
):
    """
    Get the list of titles for a specific bill.
    """
    return get_bill_titles(congress, bill_type, bill_number, API_KEY)

@router.get("/committee-details/", response_model=CommitteeResponse, summary="Get details about a specific committee")
def committee_details(
    chamber: str = Query(..., description="The chamber (house, senate, or nochamber)."),
    committee_code: str = Query(..., description="The committee code.")
):
    """
    Get detailed information about a specific committee.
    """
    print(chamber)
    print(committee_code)
    comm_detailes = get_committee_details( chamber, committee_code, API_KEY)
    print('comm_detailes')
    print(comm_detailes)
    return comm_detailes

@router.get("/house-communications/", response_model=CommunicationResponse, summary="Get House communications")
def house_communications(
    congress: int = Query(..., description="The congress number."),
    communication_type: str = Query(..., description="The type of communication (ec, ml, pm, pt).")
):
    """
    Get a list of House communications based on congress and type.
    """
    house_comms = get_house_communications(congress, communication_type, API_KEY)
    print("house_comms")
    print(house_comms)
    return house_comms

@router.get("/senate-communications/", response_model=SenateCommunicationResponse, summary="Get Senate communications")
def senate_communications(
    congress: int = Query(..., description="The congress number."),
    communication_type: str = Query(..., description="The type of communication (ec, pm, pom).")
):
    """
    Get a list of Senate communications based on congress and type.
    """
    return get_senate_communications(congress, communication_type, API_KEY)