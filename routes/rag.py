from fastapi import APIRouter, Body
from DB.chroma_connector import load_chroma

router = APIRouter()
retriever = load_chroma().as_retriever()

@router.post("/rag-search")
def rag_search(prompt: str = Body(..., embed=True)):
    docs = retriever.get_relevant_documents(prompt)
    return {"results": [doc.page_content for doc in docs]}