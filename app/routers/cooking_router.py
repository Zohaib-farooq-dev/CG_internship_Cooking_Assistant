from fastapi import APIRouter
from app.models.query import QueryRequest
from app.services import query_services

router = APIRouter()

@router.post("/process")
async def process_query(request: QueryRequest):
    return await query_services.process_query(request)