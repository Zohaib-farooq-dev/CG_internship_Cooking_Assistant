from fastapi import FastAPI
from app.routers import cooking_router

app = FastAPI(title="LangGraph API")

app.include_router(cooking_router.router)




