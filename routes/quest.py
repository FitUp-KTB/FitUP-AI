from fastapi import APIRouter
from sqlalchemy.orm import Session
from chains.quest_chain import run_quest_chain
from models.io import QuestInput, QuestOutput
from DB.postgres_connector import engine
from models.quest_db import QuestRecord

router = APIRouter()

@router.post("/generate-quest", response_model=QuestOutput)
async def generate_quest(input_data: QuestInput):
    result = run_quest_chain(input_data)
    save_quest_result(user_id=input_data.user_id, result=result.model_dump())
    return result