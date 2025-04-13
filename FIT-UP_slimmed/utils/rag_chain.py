from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from prompts.rag_prompt import rag_quest_prompt
from DB.chroma_connector import load_chroma
from models.io import QuestInput
from utils.user_doc_generator import create_user_document
from langchain_core.documents import Document
import os
import json
from dotenv import load_dotenv

load_dotenv()

# OpenAI LLM 설정
llm = ChatOpenAI(
    model_name="gpt-3.5-turbo",
    temperature=0.5,
    api_key=os.getenv("OPENAI_API_KEY")
)

def generate_quest_with_rag(input_data: QuestInput) -> str:
    # 1. 사용자 정보로 문서 생성
    user_doc_text = create_user_document(input_data)
    doc = Document(page_content=user_doc_text)

    # 2. 벡터 DB에 문서 저장
    vectorstore = load_chroma()
    vectorstore.add_documents([doc])
    retriever = vectorstore.as_retriever()

    # 3. 사용자 쿼리 기반 문서 검색
    query = f"{input_data.chronic} {input_data.user_request} {input_data.goal}"
    docs = retriever.get_relevant_documents(query)
    context = "\n\n".join([doc.page_content for doc in docs[:3]])

    # 4. LLM 프롬프트 입력 구성
    inputs = {
        "user_id": input_data.user_id,
        "gender": input_data.gender,
        "chronic": input_data.chronic,
        "stats": json.dumps(input_data.stats, ensure_ascii=False),
        "main_category": input_data.main_category,
        "sub_category": input_data.sub_category,
        "user_request": input_data.user_request,
        "goal": input_data.goal,
        "context": context
    }

    # 5. LLMChain 실행
    chain = LLMChain(llm=llm, prompt=rag_quest_prompt)
    return chain.run(inputs)