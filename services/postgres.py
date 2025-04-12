# services/postgres.py
# services/ 폴더는 "DB 활용"과 관련된 서비스들을 모아놓은 폴더

from models.quest_db import QuestRecord
from DB.postgres_connector import SessionLocal

def save_to_postgres(result: QuestRecord): # PostgreSQL에 퀘스트 기록 저장
    db = SessionLocal()
    db.add(result)
    db.commit()
    db.close()

def fetch_quests_from_db(user_id: str): # PostgreSQL에서 퀘스트 기록 
    db = SessionLocal()
    records = db.query(QuestRecord).filter_by(user_id=user_id).all()
    db.close()
    return [r.__dict__ for r in records]