from fastapi import FastAPI
from app.api.endpoints import members

app = FastAPI(
    title="Chat with Congress",
    description="This API allows users to interact with data pulled from the Congress.gov API.",
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
