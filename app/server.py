from __future__ import annotations
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
from neo4j import exceptions
from app.genai import get_neo4j_response
import logging

logging.basicConfig(level=logging.DEBUG)


class ApiChatPostRequest(BaseModel):
    message: str = Field(..., description="The chat message to send")
    retriever: str = Field(
        "neo4j",
        description='Retriever to use. Current options are: "weaviate", "pinecone", "neo4j". Default is "neo4j"',
    )


class ApiChatPostResponse(BaseModel):
    response: str


class Neo4jExceptionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except exceptions.AuthError as e:
            msg = f"Neo4j Authentication Error: {e}"
            logging.warning(msg)
            return Response(content=msg, status_code=400, media_type="text/plain")
        except exceptions.ServiceUnavailable as e:
            msg = f"Neo4j Database Unavailable Error: {e}"
            logging.warning(msg)
            return Response(content=msg, status_code=400, media_type="text/plain")
        except Exception as e:
            msg = f"Neo4j Uncaught Exception: {e}"
            logging.error(msg)
            return Response(content=msg, status_code=400, media_type="text/plain")


# Allowed CORS origins
origins = [
    "http://127.0.0.1:8000",  # Alternative localhost address
    "http://localhost:8000",
]

app = FastAPI()

# Add CORS middleware to allow cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Add Neo4j exception handling middleware
app.add_middleware(Neo4jExceptionMiddleware)


@app.post(
    "/api/chat",
    response_model=None,
    responses={"201": {"model": ApiChatPostResponse}},
    tags=["chat"],
)
async def send_chat_message(body: ApiChatPostRequest):
    """
    Send a chat message
    """

    question = body.message
    retriever = body.retriever

    if retriever == "weaviate":
        return "Not yet implemented", 500
    elif retriever == "pinecone":
        return "Not yet implemented", 500
    else:
        response = get_neo4j_response(question)

    return response, 200
