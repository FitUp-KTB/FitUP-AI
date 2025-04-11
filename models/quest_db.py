from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class QuestRecord(Base):
    __tablename__ = "quests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)
    result_json = Column(JSON)  # 전체 퀘스트 결과 저장

from fastapi import APIRouter
from sqlalchemy.orm import Session
from chains.quest_chain import run_quest_chain
from models.io import QuestInput, QuestOutput
from DB.postgres_connector import engine
from models.quest_db import QuestRecord

router = APIRouter()

@router.post("/generate-quest", response_model=QuestOutput)
def generate_quest(input_data: QuestInput):
    result = run_quest_chain(input_data)

    # PostgreSQL 저장
    with Session(engine) as session:
        quest_record = QuestRecord(
            user_id=input_data.user_id,
            result_json=result.model_dump()
        )
        session.add(quest_record)
        session.commit()

    return result