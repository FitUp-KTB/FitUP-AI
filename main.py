from fastapi import FastAPI 
from routes import quest, rag 

app = FastAPI()

app.include_router(quest.router) # Include the quest router
app.include_router(rag.router) # Include the RAG router
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.rag import router as rag_router

app = FastAPI()

# 👇 CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 origin 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 포함
app.include_router(rag_router)
