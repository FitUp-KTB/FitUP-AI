from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# 사용자 입력 모델 정의
class UserInput(BaseModel):
    user_id: str
    gender: str
    chronic: str
    stats: dict
    main_category: str
    sub_category: str
    user_request: str
    goal: str

# 예시 기존 기록 (실제 서비스에서는 DB에서 관리)
documents = [
    "스쿼트 80kg 5세트 수행",
    "레그 익스텐션 50kg 5세트",
    "레그프레스 160kg 5세트",
    "수면 8시간 유지",
    "아침 공복에 물 500ml 마시기"
]

# 임베딩 및 FAISS 벡터 DB 초기화
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_texts(documents, embeddings)
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# LLM 초기화 (OPENAI_API_KEY는 .env 파일에서 로드)
llm = OpenAI(temperature=0)

# JSON 포맷 출력 위한 프롬프트 템플릿 (출력 예시의 중괄호는 이스케이프 처리)
prompt_template_str = """
너는 사람들의 운동을 돕는 게임 기반의 퀘스트 생성 시스템이야.
입력 데이터는 아래 JSON 형식으로 주어진다:
{input_data}

사용자 요청은 다음과 같다:
{user_request}

검색된 기존 기록은 아래와 같이 주어진다:
{retrieved_records}

추가로, 너는 RAG를 사용해서 검색된 기존 기록(예: 이전 퀘스트 수행 내역 등)을 참고 자료로 활용할 거야.
이 검색된 기록은 퀘스트 생성 시, 목표(goal) 및 참고 사항으로만 사용돼.

[규칙]
1. daily_quests의 daily:
   - 목표에 맞는 식단이나 생활습관 등 관련 퀘스트를 생성할 것.
   - 오직 goal과 검색된 기존 기록에 영향을 받아 구성할 것.
2. daily_quests의 fitness:
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

prompt_template = PromptTemplate(
    input_variables=["input_data", "user_request", "retrieved_records"],
    template=prompt_template_str,
)

llm_chain = LLMChain(llm=llm, prompt=prompt_template)

@app.post("/query")
async def query_endpoint(input_data: UserInput):
    # 사용자 요청에 따른 관련 문서 검색
    retrieved_docs = retriever.get_relevant_documents(input_data.user_request)
    retrieved_records_text = " ".join([doc.page_content for doc in retrieved_docs])
    
    # LangChain 체인을 통해 최종 JSON 생성
    final_output = llm_chain.run({
        "input_data": str(input_data.dict()),
        "user_request": input_data.user_request,
        "retrieved_records": retrieved_records_text
    })
    
    return final_output