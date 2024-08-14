"""
Unit tests for all endpoints.
"""

from fastapi.testclient import TestClient
from app.api.main import app
import tiktoken
from app.api.models.requests import (BillAmendmentResponse)

client = TestClient(app)

def calculate_tokens(text):
    encoding = tiktoken.get_encoding("cl100k_base")
    return len(encoding.encode(text))

def test_search_members():
    # Direct API call to search for members
    response = client.post("/search-members/", json={"name": "John Doe"})
    
    # Validate the response
    assert response.status_code == 200
    response_json = response.json()
    
    assert "members" in response_json
    assert len(response_json["members"]) > 0
    assert calculate_tokens(response.text) < 4096, "Response exceeded token limit"


def test_get_member_details():
    # First, search for a member to get the bioguideId
    search_response = client.post("/search-members/", json={"name": "John Doe"})
    print(search_response)
    assert search_response.status_code == 200
    search_json = search_response.json()

    # Assuming the first member in the list is valid for testing
    bioguide_id = search_json["members"][0]["bioguideId"]
    print(bioguide_id)
    # Get member details using the bioguideId
    response = client.post("/member-details/", json={"member_id": bioguide_id})
    
    # Validate the response
    assert response.status_code == 200
    response_json = response.json()
    print("response_json")
    print(response_json)
    # Check the nested "member" key in the response
    assert response_json["bioguideId"] == bioguide_id
    assert calculate_tokens(response.text) < 4096, "Response exceeded token limit"




def test_chat():
    # Assuming 'A000360' is a valid member_id for testing
    response = client.post("/chat/", json={"question": "Tell me about the roles", "member_id": "A000360"})
    
    # Validate the response
    assert response.status_code == 200
    assert "response" in response.json()
    assert "score" in response.json()
    assert calculate_tokens(response.text) < 4096, "Response exceeded token limit"

def test_get_bill_details():
    # Direct API call to get bill details
    response = client.get("/bill-details/", params={"congress": 117, "bill_type": "hr", "bill_number": 3076})
    
    # Validate the response
    assert response.status_code == 200
    response_json = response.json()
    
    # Check the structure of the response
    assert "bill" in response_json
    assert "number" in response_json["bill"]
    assert response_json["bill"]["number"] == "3076"

def test_get_bill_actions():
    response = client.get("/bill-actions/", params={"congress": 117, "bill_type": "hr", "bill_number": 3076})
    assert response.status_code == 200
    
    response_json = response.json()
    assert "actions" in response_json
    assert isinstance(response_json["actions"], list)
    
    # Ensure at least one action is returned
    assert len(response_json["actions"]) > 0
    
    # Check the structure of the first action
    action = response_json["actions"][0]
    assert "actionCode" in action or "sourceSystem" in action


    
    # Additional assertions can be added as necessary


def test_get_bill_amendments():
    # Direct API call to get bill amendments
    response = client.get("/bill-amendments/", params={"congress": 117, "bill_type": "hr", "bill_number": 3076})
    
    # Validate the response
    assert response.status_code == 200
    assert "amendments" in response.json()
    assert calculate_tokens(response.text) < 4096
    
    # Validate against the Pydantic model
    amendments = BillAmendmentResponse(**response.json())
    assert len(amendments.amendments) > 0  # Ensure there are amendments in the response
    
    # Check optional fields
    for amendment in amendments.amendments:
        assert amendment.congress == 117
        assert amendment.number is not None
        assert amendment.type is not None
        assert amendment.updateDate is not None
        assert amendment.url is not None
        if amendment.description:
            assert isinstance(amendment.description, str)
        if amendment.latestAction:
            assert isinstance(amendment.latestAction.text, str)




def test_get_bill_cosponsors():
    # Direct API call to get bill cosponsors
    response = client.get("/bill-cosponsors/", params={"congress": 117, "bill_type": "hr", "bill_number": 3076})
    
    # Validate the response
    assert response.status_code == 200
    assert "cosponsors" in response.json()
    assert calculate_tokens(response.text) < 4096

def test_get_bill_related_bills():
    # Direct API call to get related bills
    response = client.get("/bill-related-bills/", params={"congress": 117, "bill_type": "hr", "bill_number": 123})
    
    # Validate the response
    assert response.status_code == 200
    assert "relatedBills" in response.json()
    assert calculate_tokens(response.text) < 4096

def test_get_bill_summaries():
    # Direct API call to get bill summaries
    response = client.get("/bill-summaries/", params={"congress": 117, "bill_type": "hr", "bill_number": 3076})
    
    # Validate the response
    assert response.status_code == 200
    assert "summaries" in response.json()
    assert calculate_tokens(response.text) < 4096

def test_get_bill_text_versions():
    # Direct API call to get bill text versions
    response = client.get("/bill-text-versions/", params={"congress": 117, "bill_type": "hr", "bill_number": 3076})
    
    # Validate the response
    assert response.status_code == 200
    assert "textVersions" in response.json()
    assert calculate_tokens(response.text) < 4096

def test_get_bill_titles():
    # Direct API call to get bill titles
    response = client.get("/bill-titles/", params={"congress": 117, "bill_type": "hr", "bill_number": 3076})
    
    # Validate the response
    assert response.status_code == 200
    assert "titles" in response.json()
    assert calculate_tokens(response.text) < 4096

def test_committee_details():
    # Direct API call to get committee details
    response = client.get("/committee-details/", params={"chamber": "house", "committee_code": "hspw00"})
    
    # Validate the response
    assert response.status_code == 200
    assert "committee" in response.json()

def test_house_communications():
    # Direct API call to get House communications
    response = client.get("/house-communications/", params={"congress": 117, "communication_type": "ec"})
    
    # Validate the response
    assert response.status_code == 200
    assert "houseCommunications" in response.json()
    assert calculate_tokens(response.text) < 4096

def test_senate_communications():
    # Direct API call to get Senate communications
    response = client.get("/senate-communications/", params={"congress": 117, "communication_type": "pm"})
    
    # Validate the response
    assert response.status_code == 200
    assert "senateCommunications" in response.json()
    assert calculate_tokens(response.text) < 4096
