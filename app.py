from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests

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

class MemberSearchRequest(BaseModel):
    name: str = Field(..., description="The name of the member of Congress to search for.")

class MemberDetailsRequest(BaseModel):
    member_id: str = Field(..., description="The ID of the member of Congress to get details for.")

class ChatRequest(BaseModel):
    question: str = Field(..., description="The question to ask about the member of Congress.")
    member_id: str = Field(..., description="The ID of the member of Congress to chat about.")

class TranscriptRequest(BaseModel):
    member_id: str = Field(..., description="The ID of the member of Congress to get transcripts for.")

@app.post("/search-members/", summary="Search for members of Congress", description="Search for members of Congress by name.")
def search_members(request: MemberSearchRequest):
    # Dummy implementation, replace with actual Congress.gov API call
    return {"members": [{"id": "A123", "name": "John Doe"}]}

@app.post("/member-details/", summary="Get details of a member of Congress", description="Get detailed information about a specific member of Congress by ID.")
def get_member_details(request: MemberDetailsRequest):
    # Dummy implementation, replace with actual Congress.gov API call
    return {"id": request.member_id, "name": "John Doe", "details": "Detailed information about John Doe."}

@app.post("/chat/", summary="Chat about a member of Congress", description="Ask questions and chat about a member of Congress using their ID.")
def chat(request: ChatRequest):
    # Dummy implementation, replace with actual chat logic
    return {"response": f"You asked about {request.member_id}: {request.question}"}

@app.post("/transcripts/", summary="Get transcripts of a member of Congress", description="Get transcripts for a specific member of Congress by ID.")
def get_transcripts(request: TranscriptRequest):
    # Dummy implementation, replace with actual Congress.gov API call
    return {"transcripts": [{"id": request.member_id, "transcript": "Transcript content here."}]}
