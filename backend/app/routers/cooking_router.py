from fastapi import APIRouter
from backend.app.models.query import QueryRequest
from backend.app.services import query_services

router = APIRouter()

@router.post("/process")
async def process_query(request: QueryRequest):
    return await query_services.process_query(request)