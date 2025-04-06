import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from IOstruct import QuestInput, QuestOutput
from prompt import quest_prompt#, prompt2

load_dotenv()
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
app = FastAPI()

# model 
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_GEMINI_API_KEY) # gemini-1.5-flash / gemini-pro

# 출력 결과 중 문자열을 선별
quest_output_parser = JsonOutputParser(pydantic_object=QuestOutput)

# chain 연결 (LCEL)
quest = quest_prompt | llm | quest_output_parser


input_dict = {
    "user_id": "12345",
    "gender": "male",
    "chronic": "척추 측만증",
    "stats": {
        "strength": 70,
        "stamina": 60,
        "endurance": 50
    },
    "main_category": "헬스",
    "sub_category": "하체",
    "user_request": "오늘은 하체 운동을 하고 싶어",
    "goal": "근력 증가",
    "last_quest_status": {
        "completed": "벤치프레스 60kg 5세트",
        "failed": "하루 2L 물 섭취"
    }
}

input_data = QuestInput(**input_dict)

@app.post("/generate-quest", response_model=QuestOutput) #output parser를 지정했지만 한번더 검증하는 용도
async def generate_quest_endpoint(input_data: QuestInput):
    result = quest.invoke({
        "input_data": input_data.model_dump()  # QuestInput → dict
    })
    return result

