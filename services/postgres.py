# services/postgres.py
# services/ 폴더는 "DB 활용"과 관련된 서비스들을 모아놓은 폴더

# FastAPI 앱 시작 전 DB 테이블 자동 생성
from models.quest_db import Base
from DB.postgres_connector import engine
Base.metadata.create_all(bind=engine) # quests 테이블이 자동으로 생성

# DB 연결 및 세션 생성
from models.quest_db import QuestRecord
from DB.postgres_connector import SessionLocal

from pydantic import BaseModel

def save_to_postgres(result):
    db = SessionLocal()

    if isinstance(result, BaseModel):
        result_dict = result.dict()
    elif isinstance(result, dict):
        result_dict = result
    else:
        raise ValueError("result는 dict 또는 Pydantic BaseModel이어야 합니다.")

    quest_record = QuestRecord(
    user_id=result_dict["user_id"],
    result_json=result_dict
    )
    db.add(quest_record)
    db.commit()
    db.close()

def fetch_quests_from_db(user_id: str): # PostgreSQL에서 퀘스트 기록 
    db = SessionLocal()
    records = db.query(QuestRecord).filter_by(user_id=user_id).all()
    db.close()
    return [r.__dict__ for r in records]