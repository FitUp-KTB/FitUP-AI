from langchain_core.output_parsers.json import JsonOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from models.io import QuestInput, QuestOutput
from prompts.prompt import quest_prompt
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    api_key=os.getenv("GEMINI_API_KEY")
)

output_parser = JsonOutputParser(pydantic_object=QuestOutput)
# LLM이 생성한 JSON을 QuestOutput이라는 Pydantic 모델객체로 변환하는 파서를 정의


chain = quest_prompt | llm | output_parser

def run_quest_chain(input_data: QuestInput) -> QuestOutput:
    return chain.invoke(input_data.model_dump())  # 이게 QuestOutput 반환하게 됨