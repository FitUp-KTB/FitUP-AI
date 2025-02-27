from flask import Flask, request, jsonify
import json
from dotenv import load_dotenv
import sqlite3
from langchain.chat_models import init_chat_model

# 환경변수 로딩
load_dotenv()

# 모델 초기화
model = init_chat_model("gpt-4o-mini", model_provider="openai")

# 데이터베이스 연결
conn = sqlite3.connect('exercise_recommendations.db')
cursor = conn.cursor()

# Flask 앱 초기화
app = Flask(__name__)

# 기본 엔드포인트 추가
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the RAG API. Use /generate_quests to generate quests."})

# 정보 검색 함수
def search_recommendation(user_query):
    cursor.execute("SELECT recommendation FROM recommendations WHERE user_message LIKE ?", ('%' + user_query + '%',))
    result = cursor.fetchone()
    return result[0] if result else "추천할 수 있는 운동이 없습니다."

# 퀘스트 생성 함수
def generate_quests(input_data):
    daily_quests = {
        "fitness": {},
        "sleep": {"contents": "수면 8시간 유지", "points": 5},
        "daily": {"contents": "아침 공복에 물 500ml 마시기", "points": 5}
    }

    if input_data["main_category"] == "부상":
        daily_quests["fitness"] = {
            1: {"contents": "휴식 및 처방을 따르세요", "points": 10}
        }
    else:
        if input_data["chronic"] == "척추 측만증":
            daily_quests["fitness"] = {
                1: {"contents": "스쿼트 60kg 3세트 수행", "points": 10},
                2: {"contents": "레그 익스텐션 40kg 5세트", "points": 5},
                3: {"contents": "레그프레스 120kg 3세트", "points": 10}
            }
        else:
            daily_quests["fitness"] = {
                1: {"contents": "스쿼트 80kg 5세트 수행", "points": 10},
                2: {"contents": "레그 익스텐션 50kg 5세트", "points": 5},
                3: {"contents": "레그프레스 160kg 5세트", "points": 20}
            }

    return {
        "user_id": input_data["user_id"],
        "daily_quests": daily_quests
    }

# LLM 호출 함수
def call_llm(input_data):
    recommendation = search_recommendation(input_data["user_request"])
    quests = generate_quests(input_data)
    
    prompt = f"""
    사용자가 요청한 내용: {input_data['user_request']}
    추천 운동: {recommendation}
    퀘스트: {json.dumps(quests, ensure_ascii=False)}
    
    다음 형식의 JSON으로 응답해 주세요:
    {{
        "status": "success",
        "data": {{
            "user_id": "{input_data['user_id']}",
            "daily_quests": {json.dumps(quests['daily_quests'], ensure_ascii=False)}
        }},
        "message": "퀘스트가 성공적으로 생성되었습니다."
    }}
    """
    
    response = model.invoke(prompt)
    return response

# API 엔드포인트 설정
@app.route('/generate_quests', methods=['POST'])
def generate_quests_endpoint():
    input_data = request.json
    if not input_data:
        return jsonify({"error": "유효한 입력 데이터가 필요합니다."}), 400
    
    try:
        response = call_llm(input_data)
        return jsonify(json.loads(response))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True)
