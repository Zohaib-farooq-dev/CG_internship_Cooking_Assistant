"""
Main entry point for the LangGraph API.

Creates a FastAPI app and includes the cooking router
to expose cooking-related endpoints.
"""

from fastapi import FastAPI
from backend.app.routers import cooking_router

app = FastAPI(title="LangGraph API")

app.include_router(cooking_router.router)




