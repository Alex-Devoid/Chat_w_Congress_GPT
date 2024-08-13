"""
Unit tests for all endpoints.
"""

from fastapi.testclient import TestClient
from app.api.main import app
from unittest.mock import patch
import tiktoken

client = TestClient(app)

def calculate_tokens(text):
    encoding = tiktoken.get_encoding("gpt-3.5-turbo")
    return len(encoding.encode(text))

def test_search_members():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"members": [{"name": "John Doe"}]}
        response = client.post("/search-members/", json={"name": "John Doe"})
        assert response.status_code == 200
        assert response.json() == {"members": [{"name": "John Doe"}]}
        assert calculate_tokens(response.text) < 4096, "Response exceeded token limit"

        mock_get.return_value.status_code = 500
        response = client.post("/search-members/", json={"name": "Jane Doe"})
        assert response.status_code == 500
        assert response.json() == {"detail": "Error fetching members"}

def test_get_member_details():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"member": {"name": "John Doe"}}
        response = client.post("/member-details/", json={"member_id": "A000360"})
        assert response.status_code == 200
        assert response.json() == {"name": "John Doe"}
        assert calculate_tokens(response.text) < 4096, "Response exceeded token limit"

        mock_get.return_value.status_code = 404
        response = client.post("/member-details/", json={"member_id": "A000360"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Member not found"}

def test_chat():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"member": {"name": "John Doe"}}
        
        response = client.post("/chat/", json={"question": "Tell me about the roles", "member_id": "A000360"})
        assert response.status_code == 200
        assert "response" in response.json()
        assert "score" in response.json()
        assert calculate_tokens(response.text) < 4096, "Response exceeded token limit"

        mock_get.return_value.status_code = 404
        response = client.post("/chat/", json={"question": "Tell me about the roles", "member_id": "A000360"})
        assert response.status_code == 404
        assert response.json() == {"detail": "Member not found"}

def test_get_bill_details():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"title": "Bill title"}
        response = client.get("/bill-details/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert response.json() == {"title": "Bill title"}
        assert calculate_tokens(response.text) < 4096

def test_get_bill_actions():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"actions": [{"actionCode": "A001", "text": "Action text"}]}
        response = client.get("/bill-actions/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "actions" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_get_bill_amendments():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"amendments": [{"congress": 117, "description": "Amendment description"}]}
        response = client.get("/bill-amendments/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "amendments" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_get_bill_cosponsors():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"cosponsors": [{"name": "Jane Doe"}]}
        response = client.get("/bill-cosponsors/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "cosponsors" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_get_bill_related_bills():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"relatedBills": [{"title": "Related Bill"}]}
        response = client.get("/bill-related-bills/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "relatedBills" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_get_bill_summaries():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"summaries": [{"text": "Summary text"}]}
        response = client.get("/bill-summaries/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "summaries" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_get_bill_text_versions():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"textVersions": [{"type": "Introduced", "url": "http://example.com"}]}
        response = client.get("/bill-text-versions/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "textVersions" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_get_bill_titles():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"titles": [{"title": "Short Title"}]}
        response = client.get("/bill-titles/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "titles" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_committee_details():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"committees": [{"name": "Committee Name"}]}
        response = client.get("/committee-details/", json={"congress": 117, "chamber": "house", "committeeCode": "ABC"})
        assert response.status_code == 200
        assert "committees" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_house_communications():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"houseCommunications": [{"number": "EC1234"}]}
        response = client.get("/house-communications/", json={"congress": 117, "communication_type": "ec"})
        assert response.status_code == 200
        assert "houseCommunications" in response.json()
        assert calculate_tokens(response.text) < 4096

def test_senate_communications():
    with patch("chat_with_congress.app.api.services.congress_api.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"senateCommunications": [{"number": "SC1234"}]}
        response = client.get("/senate-communications/", json={"congress": 117, "communication_type": "pm"})
        assert response.status_code == 200
        assert "senateCommunications" in response.json()
        assert calculate_tokens(response.text) < 4096
