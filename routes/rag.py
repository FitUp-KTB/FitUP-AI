from fastapi import APIRouter, Body
from DB.chroma_connector import load_chroma

from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA

router = APIRouter()

# 벡터 DB 로드 및 검색기 초기화
retriever = load_chroma().as_retriever()

# HuggingFace 기반 LLM 사용
llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5})

# RAG 체인 생성
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@router.post("/rag-search")
def rag_search(prompt: str = Body(..., embed=True)):
    response = rag_chain.run(prompt)
    return {"query": prompt, "response": response}