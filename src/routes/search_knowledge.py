"API routes to search the content in the FAISS"

import os
from fastapi import APIRouter, HTTPException

from src.create_knowledgebase import FAISS

router = APIRouter()

@router.get("/search_knowledge")
def search_knowledge(
    query:str,
    user_id: str
):
    try:
        retrived_knowledge = FAISS.similarity_search(
            query=query,
            unique_user_id=user_id
        )

        return retrived_knowledge
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, description="Could not search the knowledge")