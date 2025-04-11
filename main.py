from fastapi import FastAPI 
from routes import quest, rag 

app = FastAPI()

app.include_router(quest.router) # Include the quest router
app.include_router(rag.router) # Include the RAG router