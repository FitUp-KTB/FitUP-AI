import os
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from IOstruct import QuestInput, QuestOutput, StatInput, StatOutput
from prompt import quest_prompt, status_prompt

load_dotenv()
GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
app = FastAPI()

# model 
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", api_key=GOOGLE_GEMINI_API_KEY) # gemini-1.5-flash / gemini-pro

# 출력 결과 중 문자열을 선별
quest_output_parser = JsonOutputParser(pydantic_object=QuestOutput)

# chain 연결 (LCEL)
quest = quest_prompt | llm | quest_output_parser

@app.post("/generate-quest") #output parser를 지정했지만 한번더 검증하는 용도
async def generate_quest_endpoint(input_data: QuestInput):
    result = quest.invoke({
        "input_data": input_data.model_dump()  # QuestInput → dict
    })
    return result

# stat 모델

status_output_parser = JsonOutputParser(pydantic_object=StatOutput)

status = status_prompt | llm | status_output_parser

@app.post("/stats")
async def compute_stats(input_data: StatInput):
    result = status.invoke({
        'input_data': input_data.model_dump()
    })
    return result
# @app.post("/stats", response_model=StatOutput)
# async def compute_stats(input_data: StatInput):
#     try:
#         print("📥 받은 입력:", input_data)
#         result = status.invoke({
#             'input_data': input_data.model_dump()
#         })
#         print("📤 LLM 응답 결과:", result)
#         return result
#     except Exception as e:
#         print("❌ 예외 발생:", str(e))
#         return {"error": str(e)}  # 임시 JSON 반환
