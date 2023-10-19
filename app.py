from fastapi import FastAPI
from src.routes import (
    add_knowledge,
    search_knowledge
)


app = FastAPI(
    description= "Knowledge base creator from screenshot"
)


app.include_router(add_knowledge.router)
app.include_router(search_knowledge.router)


app.get("/home")
def home():
    return {"message": "WELCOME TO THE HOME"}