from langchain.prompts import ChatPromptTemplate

quest_prompt = ChatPromptTemplate.from_template("""
당신은 사용자에게 맞춤 운동 퀘스트를 추천하는 AI입니다.

[사용자 정보]
- 성별: {gender}
- 만성 질환: {chronic}
- 체력 정보: {stats}
- 메인 카테고리: {main_category}
- 서브 카테고리: {sub_category}
- 요청: {user_request}
- 목표: {goal}

[출력 형식은 JSON이며 아래와 같은 형태로 생성해주세요.]
{{
  "user_id": "{user_id}",
  "daily_quests": {{
    "fitness": {{
      "0": {{ "contents": "런지 3세트", "points": 10 }},
      "1": {{ "contents": "레그프레스 3세트", "points": 10 }}
    }},
    "sleep": {{ "contents": "7시간 이상 수면", "points": 5 }},
    "daily": {{ "contents": "2L 물 마시기", "points": 5 }}
  }}
}}
""")