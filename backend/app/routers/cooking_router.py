from fastapi import APIRouter
from backend.app.models.query import QueryRequest
from backend.app.services import query_services

router = APIRouter()

@router.post("/process")
async def process_query(request: QueryRequest)->dict:
    """
    Process a cooking-related user query.

    Args:
        request (QueryRequest): The validated request body containing the user query.

    Returns:
        dict: A dictionary containing the processed query result.
    """
    return await query_services.process_query(request)