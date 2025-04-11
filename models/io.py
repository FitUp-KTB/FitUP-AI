from pydantic import BaseModel, RootModel
from typing import Dict

class QuestInput(BaseModel):
    user_id: str
    gender: str
    chronic: str
    stats: dict
    main_category: str
    sub_category: str
    user_request: str
    goal: str

# 퀘스트 항목 기본 구조
class QuestItem(BaseModel):
    contents: str
    points: int

# fitness는 숫자 키를 가진 딕셔너리
class FitnessQuest(RootModel):
    Dict[int, QuestItem]

# 전체 daily_quests 구조
class DailyQuests(BaseModel):
    fitness: FitnessQuest
    sleep: QuestItem
    daily: QuestItem

# 최상위 출력 모델
class QuestOutput(BaseModel):
    user_id: str
    daily_quests: DailyQuests