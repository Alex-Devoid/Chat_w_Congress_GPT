from fastapi import APIRouter, HTTPException, Query, Depends, Security
from fastapi.exceptions import RequestValidationError
from fastapi.security.api_key import APIKeyHeader
from fastapi.encoders import jsonable_encoder
from starlette.status import HTTP_403_FORBIDDEN



from app.api.models.requests import (
    MemberSearchRequest, MemberDetailsRequest, ChatRequest, MembersResponse, 
    MemberDetailsResponse, ChatResponse, BillRequest, BillActionResponse, 
    BillAmendmentResponse, CommitteeRequest, CommitteeResponse, 
    CommunicationRequest, CommunicationResponse, SenateCommunicationResponse, BillRelatedResponse,
    BillCosponsorResponse, BillSummaryResponse, BillTextResponse,
    BillTitleResponse,BillDetailResponse,CommitteeResponseBill,
    CommitteeMeetingResponse,CommitteePrintResponse,BillSubjectResponse
)
from app.api.services.congress_api import (
    get_member_details, search_members, get_bill_details, get_bill_actions, 
    get_bill_amendments, get_committee_details, get_house_communications, 
    get_senate_communications, get_bill_committees, get_bill_cosponsors, 
    get_bill_related_bills, get_bill_summaries, get_bill_text_versions, 
    get_bill_titles,get_committee_prints,get_committee_meetings,get_bill_subjects
)
from app.api.services.chunking import chunk_text
from app.api.services.semantic_search import semantic_search
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

API_KEY = os.getenv("CONGRESS_GOV_API_KEY")
SERVER_API_KEY = os.getenv("SERVER_API_KEY")


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def get_api_key(api_key_header: str = Security(api_key_header)):

    if api_key_header == SERVER_API_KEY:
        return api_key_header
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

@router.post("/search-members/", response_model=MembersResponse, summary="Search for members of Congress")
def search_members_post(request: MemberSearchRequest, api_key: str = Depends(get_api_key)):
    """
    Search for members of Congress by name.
    Returns a list of members matching the search criteria.
    """

    response = search_members(api_key=API_KEY, query=request.name)


    return {"members": response.get('members', [])}

@router.post("/member-details/", response_model=MemberDetailsResponse, summary="Get details of a member of Congress")
def fetch_member_details(request: MemberDetailsRequest, api_key: str = Depends(get_api_key)):
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

    member_data = member_details_response.get('member')
    if member_data is None:
        raise HTTPException(status_code=500, detail="Unexpected response format")
    return member_data

@router.post("/chat/", response_model=ChatResponse, summary="Chat about a member of Congress")
def chat(request: ChatRequest, api_key: str = Depends(get_api_key)):
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
def bill_details(congress: int, bill_type: str, bill_number: int, api_key: str = Depends(get_api_key)):
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
    bill_number: int = Query(..., description="The bill's assigned number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get the list of actions on a specified bill.
    Returns the actions taken on the bill.
    """
    response = get_bill_actions(congress, bill_type, bill_number, API_KEY)
    return response

@router.get("/bill-amendments/", response_model=BillAmendmentResponse, summary="Get amendments related to a bill")
def bill_amendments(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hres, sres)."),
    bill_number: int = Query(..., description="The bill number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get the list of amendments to a specified bill.
    Returns the amendments associated with the bill.
    """
    amendments = get_bill_amendments(congress, bill_type, bill_number, API_KEY)
    return amendments

@router.get("/bill-cosponsors/", response_model=BillCosponsorResponse, summary="Get cosponsors of a bill")
def bill_cosponsors(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hres, sres)."),
    bill_number: int = Query(..., description="The bill number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get the list of cosponsors of a specific bill.
    """
    return get_bill_cosponsors(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-committees/", response_model=CommitteeResponseBill, summary="Get committees related to a bill")
def bill_committees(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get the list of committees associated with a specific bill.
    """
    bill_committees_response = get_bill_committees(congress, bill_type, bill_number, API_KEY)
    return bill_committees_response

@router.get("/bill-related-bills/", response_model=BillRelatedResponse, summary="Get related bills")
def bill_related_bills(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get the list of bills related to a specific bill.
    """
    return get_bill_related_bills(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-summaries/", response_model=BillSummaryResponse, summary="Get bill summaries")
def bill_summaries(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get summaries of a specific bill.
    """
    return get_bill_summaries(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-text-versions/", response_model=BillTextResponse, summary="Get bill text versions")
def bill_text_versions(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get different text versions of a specific bill.
    """
    return get_bill_text_versions(congress, bill_type, bill_number, API_KEY)

@router.get("/bill-titles/", response_model=BillTitleResponse, summary="Get bill titles")
def bill_titles(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get the list of titles for a specific bill.
    """
    return get_bill_titles(congress, bill_type, bill_number, API_KEY)

@router.get("/committee-details/", response_model=CommitteeResponse, summary="Get details about a specific committee")
def committee_details(
    chamber: str = Query(..., description="The chamber (house, senate, or nochamber)."),
    committee_code: str = Query(..., description="The committee code."),
    api_key: str = Depends(get_api_key)
):
    """
    Get detailed information about a specific committee.
    """
    comm_details = get_committee_details(chamber, committee_code, API_KEY)
    return comm_details

@router.get("/house-communications/", response_model=CommunicationResponse, summary="Get House communications")
def house_communications(
    congress: int = Query(..., description="The congress number."),
    communication_type: str = Query(..., description="The type of communication (ec, ml, pm, pt)."),
    api_key: str = Depends(get_api_key)
):
    """
    Get a list of House communications based on congress and type.
    """
    house_comms = get_house_communications(congress, communication_type, API_KEY)
    return house_comms

@router.get("/senate-communications/", response_model=SenateCommunicationResponse, summary="Get Senate communications")
def senate_communications(
    congress: int = Query(..., description="The congress number."),
    communication_type: str = Query(..., description="The type of communication (ec, pm, pom)."),
    api_key: str = Depends(get_api_key)
):
    """
    Get a list of Senate communications based on congress and type.
    """
    return get_senate_communications(congress, communication_type, API_KEY)

@router.get("/bill-subjects/", response_model=BillSubjectResponse, summary="Get bill subjects")
def bill_subjects(
    congress: int = Query(..., description="The congress number."),
    bill_type: str = Query(..., description="The bill type (e.g., hr, s, hjres, etc.)."),
    bill_number: int = Query(..., description="The bill's assigned number."),
    api_key: str = Depends(get_api_key)
):
    """
    Get the list of legislative subjects on a specified bill.
    Returns the subjects and policy area associated with the bill.
    """
    response = get_bill_subjects(congress, bill_type, bill_number, API_KEY)
    subjects = response.get("subjects", {})
    return {
        "legislativeSubjects": subjects.get("legislativeSubjects", []),
        "policyArea": subjects.get("policyArea", {})
    }

@router.get("/committee-prints/", response_model=CommitteePrintResponse, summary="Get committee prints")
def committee_prints(
    congress: int = Query(..., description="The congress number."),
    chamber: str = Query(..., description="The chamber name (house, senate, or nochamber)."),
    api_key: str = Depends(get_api_key)
):
    """
    Get a list of committee prints filtered by the specified congress and chamber.
    Returns the committee prints.
    """
    response = get_committee_prints(congress, chamber, API_KEY)
    return {"committeePrints": response.get("committeePrints", [])}

@router.get("/committee-meetings/", response_model=CommitteeMeetingResponse, summary="Get committee meetings")
def committee_meetings(
    congress: int = Query(..., description="The congress number."),
    chamber: str = Query(..., description="The chamber name (house, senate, or nochamber)."),
    api_key: str = Depends(get_api_key)
):
    """
    Get a list of committee meetings filtered by the specified congress and chamber.
    Returns the committee meetings.
    """
    response = get_committee_meetings(congress, chamber, API_KEY)
    return {"committeeMeetings": response.get("committeeMeetings", [])}
