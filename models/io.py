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
# contents: 퀘스트 내용, points: 포인트
class QuestItem(BaseModel):
    contents: str
    points: int

# fitness는 숫자 키를 가진 딕셔너리
# 0, 1, 2... 등으로 퀘스트 항목을 구분
class FitnessQuest(RootModel):
    Dict[int, QuestItem]

# 전체 daily_quests 구조

class DailyQuests(BaseModel):
    fitness: FitnessQuest # 운동 관련 퀘스트
    sleep: QuestItem # 수면 관련 퀘스트
    daily: QuestItem # 일상 관련 퀘스트

# 최상위 출력 모델
# user_id: 사용자 ID
# daily_quests: DailyQuests 모델을 사용하여 퀘스트 항목을 포함
# 하루치 추천 퀘스트를 JSON 형태로 반환
class QuestOutput(BaseModel):
    user_id: str
    daily_quests: DailyQuests