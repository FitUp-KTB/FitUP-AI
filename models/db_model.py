from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QuestLog(Base):
    __tablename__ = "quest_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)
    goal = Column(String)
    main_category = Column(String)
    sub_category = Column(String)
    quests = Column(JSON)  # 전체 퀘스트 JSON 저장

### DB 초기화 및 테이블 생성(한번만 실행만 하면 됨)
from DB.postgres_connector import engine
from models.db_model import Base

Base.metadata.create_all(bind=engine)