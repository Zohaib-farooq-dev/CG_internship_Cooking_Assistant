"""
API router for cooking-related queries.

Provides endpoints to process user queries and return
responses from the query services layer.
"""
from fastapi import APIRouter
from backend.app.models.query import QueryRequest
from backend.app.services import query_services

router = APIRouter()

@router.post("/process")
async def process_query(request: QueryRequest)->dict:
    """ Accept the user query from request body and pass it to a fucntion to process it."""
    return await query_services.process_query(request)