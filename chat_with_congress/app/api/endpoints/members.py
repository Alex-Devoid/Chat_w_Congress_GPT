@app.post("/search-members/", summary="Search for members of Congress", description="Search for members of Congress by name.")
def search_members(request: MemberSearchRequest):
    """
    Search for members of Congress by name.
    Returns a list of members matching the search criteria.
    """
    response = requests.get(f"{BASE_URL}/member", params={"query": request.name, "api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/member-details/", summary="Get details of a member of Congress", description="Get detailed information about a specific member of Congress by ID.")
def get_member_details(request: MemberDetailsRequest):
    """
    Get detailed information about a specific member of Congress by ID.
    Returns the member's details including name, bio, and roles.
    """
    response = requests.get(f"{BASE_URL}/member/{request.member_id}", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/chat/", summary="Chat about a member of Congress", description="Ask questions and chat about a member of Congress using their ID.")
def chat(request: ChatRequest):
    """
    Chat about a member of Congress using their ID.
    Responds to questions about the specified member.
    """
    # Dummy implementation, replace with actual chat logic
    return {"response": f"You asked about {request.member_id}: {request.question}"}

@app.post("/transcripts/", summary="Get transcripts of a member of Congress", description="Get transcripts for a specific member of Congress by ID.")
def get_transcripts(request: TranscriptRequest):
    """
    Get transcripts for a specific member of Congress by ID.
    Returns the member's speech transcripts.
    """
    response = requests.get(f"{BASE_URL}/member/{request.member_id}/transcripts", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-details/", summary="Get details of a bill", description="Get detailed information about a specific bill.")
def get_bill_details(request: BillRequest):
    """
    Get detailed information about a specific bill.
    Returns details including title, summary, and status.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-actions/", summary="Get actions of a bill", description="Get the list of actions on a specified bill.")
def get_bill_actions(request: BillRequest):
    """
    Get the list of actions on a specified bill.
    Returns the actions taken on the bill.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/actions", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-amendments/", summary="Get amendments of a bill", description="Get the list of amendments on a specified bill.")
def get_bill_amendments(request: BillRequest):
    """
    Get the list of amendments on a specified bill.
    Returns the amendments proposed to the bill.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/amendments", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-committees/", summary="Get committees of a bill", description="Get the list of committees associated with a specified bill.")
def get_bill_committees(request: BillRequest):
    """
    Get the list of committees associated with a specified bill.
    Returns the committees reviewing the bill.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/committees", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-cosponsors/", summary="Get cosponsors of a bill", description="Get the list of cosponsors on a specified bill.")
def get_bill_cosponsors(request: BillRequest):
    """
    Get the list of cosponsors on a specified bill.
    Returns the bill's cosponsors.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/cosponsors", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-relatedbills/", summary="Get related bills", description="Get the list of related bills to a specified bill.")
def get_bill_relatedbills(request: BillRequest):
    """
    Get the list of related bills to a specified bill.
    Returns bills related to the specified bill.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/relatedbills", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-subjects/", summary="Get subjects of a bill", description="Get the list of legislative subjects on a specified bill.")
def get_bill_subjects(request: BillRequest):
    """
    Get the list of legislative subjects on a specified bill.
    Returns subjects associated with the bill.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/subjects", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-summaries/", summary="Get summaries of a bill", description="Get the list of summaries for a specified bill.")
def get_bill_summaries(request: BillRequest):
    """
    Get the list of summaries for a specified bill.
    Returns the bill's summaries.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/summaries", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-text/", summary="Get text of a bill", description="Get the list of text versions for a specified bill.")
def get_bill_text(request: BillRequest):
    """
    Get the list of text versions for a specified bill.
    Returns the bill's text versions.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/text", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/bill-titles/", summary="Get titles of a bill", description="Get the list of titles for a specified bill.")
def get_bill_titles(request: BillRequest):
    """
    Get the list of titles for a specified bill.
    Returns the bill's titles.
    """
    response = requests.get(f"{BASE_URL}/bill/{request.congress}/{request.bill_type}/{request.bill_number}/titles", params={"api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/committee-print/", summary="Get committee prints", description="Get a list of committee prints.")
def get_committee_prints(request: CommitteePrintRequest):
    """
    Get a list of committee prints.
    Returns committee prints filtered by congress and chamber.
    """
    response = requests.get(f"{BASE_URL}/committee-print/{request.congress}/{request.chamber}", params={"jacketNumber": request.jacket_number, "api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/committee-meeting/", summary="Get committee meetings", description="Get a list of committee meetings.")
def get_committee_meetings(request: CommitteeMeetingRequest):
    """
    Get a list of committee meetings.
    Returns committee meetings filtered by congress and chamber.
    """
    response = requests.get(f"{BASE_URL}/committee-meeting/{request.congress}/{request.chamber}", params={"eventId": request.event_id, "api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/house-communication/", summary="Get House communications", description="Get a list of House communications.")
def get_house_communications(request: CommunicationRequest):
    """
    Get a list of House communications.
    Returns House communications filtered by congress and communication type.
    """
    response = requests.get(f"{BASE_URL}/house-communication/{request.congress}/{request.communication_type}", params={"communicationNumber": request.communication_number, "api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()

@app.post("/senate-communication/", summary="Get Senate communications", description="Get a list of Senate communications.")
def get_senate_communications(request: CommunicationRequest):
    """
    Get a list of Senate communications.
    Returns Senate communications filtered by congress and communication type.
    """
    response = requests.get(f"{BASE_URL}/senate-communication/{request.congress}/{request.communication_type}", params={"communicationNumber": request.communication_number, "api_key": API_KEY})
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching data from Congress.gov API")
    return response.json()
