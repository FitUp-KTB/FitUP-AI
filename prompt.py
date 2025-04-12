from langchain_core.prompts import ChatPromptTemplate

quest_prompt = ChatPromptTemplate.from_template(
"""
너는 사람들의 운동을 돕는 게임 기반의 퀘스트 생성 시스템이야.
입력 데이터는 아래 JSON 형식으로 주어진다:
{input_data}

추가로, 너는 RAG를 사용해서 검색된 기존 기록(예: 이전 퀘스트 수행 내역 등)을 참고 자료로 활용할 거야.
이 검색된 기록은 퀘스트 생성 시, 목표(goal) 및 참고 사항으로만 사용돼. 꼭 검색 기록에서만 퀘스트를 만들 필요 없이 내용이 부족한거같으면 너가 생성해줘도 돼

[규칙]
1. daily_quests의 daily:
   - 목표에 맞는 식단이나 생활습관 등 관련 퀘스트를 생성할 것.
   - 오직 goal과 검색된 기존 기록에 영향을 받아 구성할 것.
2. daily_quests의 fitness:
   - 총 3개 퀘스트 생성
   - 입력 데이터의 main_category, sub_category, user_request, goal, stats, gender, chronic을 반영하여 운동 종목과 난이도를 조정할 것.
   - 운동 종목은 최대한 세부적으로 선정하고, 세트 운동인 경우 "몇kg 몇개 몇세트" 형식으로 명시할 것.
   - 만약 chronic 값이 주어지면, 해당 질환(예: 척추 측만증)에 따라 운동 강도나 종목 선택을 조정할 것.
3. 만약 main_category가 "부상"이라면:
   - sub_category는 없으며, user_request에 부상 부위와 증상 내용이 포함되므로, daily_quests의 fitness는 운동 대신 처방이나 휴식 관리를 추천할 것.
4. 모든 퀘스트에는 수행 완료 시 포인트를 부여:
   - 운동 카테고리는 난이도에 따라 쉬움(5점), 보통(10점), 어려움(20점)으로 결정할 것.
   - 수면(sleep)과 생활습관(daily) 퀘스트는 5점으로 고정할 것.
5. 다음과 같은 형태의 출력이 나오도록 할 것
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

답변은 반드시 Json으로만 출력해줘.
"""
)

status_prompt = ChatPromptTemplate.from_template(
"""
너는 신체 스펙 데이터와 운동 수행능력 데이터를 받아서 스펙으로 반환해줄거야 
입력 데이터는 
{input_data}
다음과 같은 json 데이터야

입력된 정보들을 가지고 스탯을 계산해줘
strength: 스쿼트, 벤치프레스, 데드리프트 무게를 기반으로 계산, 높은 무게를 들수록 높은 점수를 얻습니다. 

endurance: 팔굽혀펴기, 윗몸일으키기 횟수를 기반으로 계산 많은 횟수를 할수록 높은 점수를 얻습니다. 

speed: 달리기 페이스를 기반으로 숫자가 낮을수록 높은 점수를 얻습니다. 

flexibility : 기본으로 50 값으로설절됩니다. 

stamina: 달리기 시간을 기반으로 계산되었습니다. 오래 달릴수록 높은 점수를 얻습니다. 또한 endurance점수와 speed점수를 적절히 반영합니다. 

character_type: strength, endurance, speed, flexibility, stamina 점수를 종합적으로 고려하여 판단 (높다는 기준은 다른 스탯 평균보다 20%이상 수치를 가질때)
{{
runner	러닝 페이스 & 유지 시간이 높음
power    근력이 높음
diet 	체지방률이 높아 유산소를 주로 수행해야 하는 체형
balance	전반적인 운동 능력이 균등하게 분포되어있음
endurance	팔굽혀펴기 & 윗몸일으키기 반복 횟수가 많음
}}

만약 입력이 들어올 때 값이 없는 항목이 있으면 내가 준 gender 별 기준값으로 채워서 사용해줘
출력형식은 다음과 같아
{{
  "user_id": "12345",
  "chronic" : "척추 측만증",
  "strength": <strength>,
  "endurance": <endurance>,
  "speed": <speed>,
  "flexibility": <flexibility>,
  "stamina": <stamina>,
  "character_type": "power"
}}
답변은 반드시 JSON 그 자체만 출력해 주세요.
"""
)