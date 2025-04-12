from fastapi import APIRouter
from models.io import QuestInput
from chains.quest_chain import run_quest_chain
from services.postgres import save_to_postgres, fetch_quests_from_db
from models.quest_db import QuestRecord

router = APIRouter()

@router.post("/generate-quest")
async def generate_quest(input_data: QuestInput):
    result = run_quest_chain(input_data)
    save_to_postgres(result)
    return result

@router.get("/quest-history/{user_id}")
async def get_history(user_id: str):
    history = fetch_quests_from_db(user_id)
    return {"quests": history}