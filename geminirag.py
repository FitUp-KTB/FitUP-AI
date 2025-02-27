from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv
import numpy as np

load_dotenv()

# Google Gemini API 키 설정
genai.configure(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))

app = FastAPI()

reference_texts = [
    # 하체 운동
    "스쿼트 80kg 5세트 수행"
    "레그프레스 100kg 5세트 수행"
    "레그 익스텐션 50kg 5세트 수행"
    "레그 컬 40kg 5세트 수행"
    "힙 쓰러스트 60kg 5세트 수행"
    "런지 15회 수행"
    "스텝업 12회 수행"
    "카프 레이즈 20회 수행"
    "스미스 머신 스쿼트 70kg 5세트 수행"
    "프론트 스쿼트 60kg 5세트 수행"
    "바벨 힙 스러스트 80kg 5세트 수행"
    "단일 다리 데드리프트 15회 수행"
    "사이드 런지 12회 수행"
    "드롭 스쿼트 10회 수행"
    "글루트 브릿지 15회 수행"
    
    # 상체 운동
    "벤치 프레스 60kg 5세트 수행"
    "푸시업 15회 수행"
    "덤벨 숄더 프레스 20kg 5세트 수행"
    "랫 풀다운 50kg 5세트 수행"
    "딥스 10회 수행"
    "덤벨 플라이 15회 수행"
    "바벨 로우 60kg 5세트 수행"
    "덤벨 컬 15회 수행"
    "트라이셉스 익스텐션 15회 수행"
    "체스트 프레스 60kg 5세트 수행"
    "케이블 로우 50kg 5세트 수행"
    "푸시 프레스 50kg 5세트 수행"
    "플랫 벤치 덤벨 프레스 15회 수행"
    "오버헤드 덤벨 트라이셉스 익스텐션 15회 수행"
    "덤벨 스컬크러셔 15회 수행"
    "페이스 풀 15회 수행"
    
    # 복근 운동
    "윗몸 일으키기 20회 수행"
    "플랭크 60초 유지"
    "사이드 플랭크 30초 유지"
    "러시안 트위스트 15회 수행"
    "레그 레이즈 15회 수행"
    "버피 10회 수행"
    "마운틴 클라이머 30초 수행"
    "크런치 20회 수행"
    "힙 레이즈 15회 수행"
    "바이시클 크런치 20회 수행"
    "플랭크 롤아웃 10회 수행"
    "앱 휠 롤아웃 10회 수행"
    "스위스 볼 크런치 15회 수행"
    "줄넘기 5분 수행"
    "탑 핀 크런치 15회 수행"
    
    # 유산소 운동
    "30분 조깅"
    "자전거 타기 1시간"
    "수영 30분"
    "스텝퍼 20분"
    "엘리프티컬 30분"
    "줄넘기 10분"
    "하이킹 1시간"
    "댄스 30분"
    "킥복싱 30분"
    "스피닝 45분"
    "트레드밀 인터벌 30분"
    "사이클링 1시간"
    "체조 30분"
    "배드민턴 1시간"
    "웨이트 트레이닝 30분"
    "크로스핏 30분"
    
    # 기타 운동
    "스트레칭 15분"
    "요가 30분"
    "필라테스 30분"
    "바이크 30분"
    "체중 운동 20분"
    "균형 훈련 15분"
    "코어 운동 20분"
    "명상 10분"
    "저항 밴드 운동 20분"
    "스텝 운동 15분"
    "디스크 훈련 15분"
    "스포츠 마사지 30분"
    "발목 강화 운동 15회 수행"
    "골반 기울이기 운동 15회 수행"
    "넓은 스쿼트 15회 수행"
    "하체 스트레칭 10분 수행"
]

embedding_model = genai.GenerativeModel("models/embedding-001")

def get_embedding(text):
    """텍스트를 임베딩 벡터로 변환"""
    response = embedding_model.generate_content(text)
    return np.array(response.text.split(","), dtype=float)  # 임베딩 값이 ','로 구분된다고 가정

def find_most_relevant_text(query, reference_texts):
    """입력된 텍스트와 가장 유사한 기존 텍스트 검색"""
    query_embedding = get_embedding(query)
    reference_embeddings = [get_embedding(text) for text in reference_texts]

    similarities = [np.dot(query_embedding, ref_emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(ref_emb))
                    for ref_emb in reference_embeddings]
    
    best_match_index = np.argmax(similarities)
    return reference_texts[best_match_index], similarities[best_match_index]

### 1. 퀘스트 생성 관련 코드 ###
class QuestInput(BaseModel):
    user_id: str
    gender: str
    chronic: str
    stats: dict
    main_category: str
    sub_category: str
    user_request: str
    goal: str

# Google Gemini LLM을 사용하여 퀘스트 생성
quest_prompt_template = """
너는 사람들의 운동을 돕는 게임 기반의 퀘스트 생성 시스템이야.
입력 데이터는 아래 JSON 형식으로 주어진다:
{input_data}

사용자 요청은 다음과 같다:
{user_request}

검색된 기존 기록은 아래와 같이 주어진다:
{retrieved_records}

추가로, 너는 RAG를 사용해서 검색된 기존 기록(예: 이전 퀘스트 수행 내역 등)을 참고 자료로 활용할 거야.
이 검색된 기록은 퀘스트 생성 시, 목표(goal) 및 참고 사항으로만 사용돼. 꼭 검색 기록에서만 퀘스트를 만들 필요 없이 내용이 부족한거같으면 너가 생성해줘도 돼

[규칙]
1. daily_quests의 daily:
   - 목표에 맞는 식단이나 생활습관 등 관련 퀘스트를 생성할 것.
   - 오직 goal과 검색된 기존 기록에 영향을 받아 구성할 것.
2. daily_quests의 fitness:
   - 총 3개 퀘스트 생성하기
   - 입력 데이터의 main_category, sub_category, user_request, goal, stats, gender, chronic을 반영하여 운동 종목과 난이도를 조정할 것.
   - 운동 종목은 최대한 세부적으로 선정하고, 세트 운동인 경우 "몇개 몇세트" 형식으로 명시할 것.
   - 만약 chronic 값이 주어지면, 해당 질환(예: 척추 측만증)에 따라 운동 강도나 종목 선택을 조정할 것.
3. 만약 main_category가 "부상"이라면:
   - sub_category는 없으며, user_request에 부상 부위와 증상 내용이 포함되므로, daily_quests의 fitness는 운동 대신 처방이나 휴식 관리를 추천할 것.
4. 모든 퀘스트에는 수행 완료 시 포인트를 부여:
   - 운동 카테고리는 난이도에 따라 쉬움(5점), 보통(10점), 어려움(20점)으로 결정할 것.
   - 수면(sleep)과 생활습관(daily) 퀘스트는 5점으로 고정할 것.
5. 최종 출력은 반드시 설명이나 상세 분석 없이 순수 JSON 형식만 반환해줘.

출력 JSON 예시:
{{
  "user_id": "12345",
  "daily_quests": {{
    "fitness": {{
      "1": {{"contents": "스쿼트 80kg 5세트 수행", "points": 10}},
      "2": {{"contents": "레그 익스텐션 50kg 5세트", "points": 5}},
      "3": {{"contents": "레그프레스 160kg 5세트", "points": 20}}
    }},
    "sleep": {{"contents": "수면 8시간 유지", "points": 5}},
    "daily": {{"contents": "아침 공복에 물 500ml 마시기", "points": 5}}
  }}
}}

반드시 JSON 형식만 출력해줘.
"""

@app.post("/query")
async def query_endpoint(input_data: QuestInput):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        quest_prompt_template.format(
            input_data=input_data.dict(),
            user_request=input_data.user_request,
            retrieved_records=reference_texts
        )
    )
    return response.text

### 2. 헬스케어 스펙 계산 관련 코드 ###
class HealthInput(BaseModel):
    user_id: str
    gender: str
    chronic: str = ""
    height: float = None
    weight: float = None
    muscle_mass: float = None
    body_fat: float = None
    pushups: int = None
    situps: int = None
    running_pace: float = None
    running_time: float = None
    squat: float = None
    bench_press: float = None
    deadlift: float = None

stats_prompt_template = """
너의 역할은 게임기반 헬스케어 서비스를 관리하는 시스템이야
기능은 신체 스펙 데이터와 운동 수행능력 데이터를 받아서 스펙으로 반환해줄거야 
데이터 형식은 다음과 같아
입력 데이터는 
{{
  "user_id": "12345",
  "gender" : "male",
  "chronic" : "척추 측만증",
  "height": 175,
  "weight": 70,
  "muscle_mass": 35,
  "body_fat": 18,
  "pushups": 40,
  "situps": 50,
  "running_pace": 5.0,
  "running_time": 30,
  "squat": 100,
  "bench_press": 80,
  "deadlift": 120
}}
형식의 JSON 파일이고

입력된 정보들을 가지고 스탯을 계산해줘
strength: 스쿼트, 벤치프레스, 데드리프트 무게를 기반으로 계산, 높은 무게를 들수록 높은 점수를 얻습니다. 

endurance: 팔굽혀펴기, 윗몸일으키기 횟수를 기반으로 계산 많은 횟수를 할수록 높은 점수를 얻습니다. 

speed: 달리기 페이스를 기반으로 숫자가 낮을수록 높은 점수를 얻습니다. 

stamina: 달리기 시간을 기반으로 계산되었습니다. 오래 달릴수록 높은 점수를 얻습니다. 또한 endurance점수와 speed점수를 합산하여 반영합니다. 

character_type: strength, endurance, speed, flexibility, stamina 점수를 종합적으로 고려하여 판단 (높다는 기준은 다른 스탯 평균보다 20%이상 수치를 가질때)
{{
runner	러닝 페이스 & 유지 시간이 높음
power    근력이 높음
diet 	체지방률이 높아 유산소를 주로 수행해야 하는 체형
balance	전반적인 운동 능력이 균등하게 분포되어있음
endurance	팔굽혀펴기 & 윗몸일으키기 반복 횟수가 많음
}}

입력 데이터의 성별이 "male"일때 각각의 모든 스탯이 50인 기준 값들은 다음과 같아.
{{
  "user_id": "12345",
  "gender" : "male",
  "chronic" : "",
  "height": 175,
  "weight": 70,
  "muscle_mass": 33,
  "body_fat": 25,
  "pushups": 40,
  "situps": 50,
  "running_pace": 4.0,
  "running_time": 30,
  "squat": 60,
  "bench_press": 60,
  "deadlift": 60
}} 

입력 데이터의 성별이 "female"일때 각각의 모든 스탯이 50인 기준 값들은 다음과 같아.
{{
  "user_id": "12345",
  "gender" : "female",
  "chronic" : "",
  "height": 166,
  "weight": 60,
  "muscle_mass": 25,
  "body_fat": 35,
  "pushups": 10,
  "situps": 30,
  "running_pace": 3.5,
  "running_time": 30,
  "squat": 40,
  "bench_press": 40,
  "deadlift": 40
}} 

만약 입력이 들어올 때 값이 없는 항목이 있으면 내가 준 gender 별 기준값으로 채워서 사용해줘
출력형식은 다음과 같아
{{
  "user_id": "12345",
  "chronic" : "척추 측만증",
  "strength": <strength>,
  "endurance": <endurance>,
  "speed": <speed>,
  "stamina": <stamina>,
  "character_type": "power"
}}
설명이나 추가 내용 없이 출력형식의 JSON만 반환
"""


@app.post("/stats")
async def compute_stats(input_data: HealthInput):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(
        stats_prompt_template.format(input_data=input_data.dict())
    )
    return response.text