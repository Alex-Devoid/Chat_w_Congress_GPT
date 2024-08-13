"""
Unit tests for all endpoints.
"""

from fastapi.testclient import TestClient
from app.api.main import app
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


def test_get_bill_details():
    with patch("chat_with_congress.app.api.endpoints.members.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"title": "Bill title"}
        response = client.get("/bill-details/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert response.json() == {"title": "Bill title"}
        assert calculate_tokens(response.json()) < 4096

def test_get_bill_actions():
    with patch("chat_with_congress.app.api.endpoints.members.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"actions": [{"actionCode": "A001", "text": "Action text"}]}
        response = client.get("/bill-actions/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "actions" in response.json()
        assert calculate_tokens(response.json()) < 4096

def test_get_bill_amendments():
    with patch("chat_with_congress.app.api.endpoints.members.requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"amendments": [{"congress": 117, "description": "Amendment description"}]}
        response = client.get("/bill-amendments/", json={"congress": 117, "bill_type": "hr", "bill_number": 123})
        assert response.status_code == 200
        assert "amendments" in response.json()
        assert calculate_tokens(response.json()) < 4096


# Repeat similar tests for all other endpoints: transcripts, bill-details, etc.
