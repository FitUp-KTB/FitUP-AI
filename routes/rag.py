from fastapi import APIRouter, Body
from DB.chroma_connector import load_chroma

from langchain.llms import HuggingFaceHub
from langchain.chains import RetrievalQA

router = APIRouter()

# 벡터 DB 로드 및 검색기 초기화
retriever = load_chroma().as_retriever()

# HuggingFace 기반 LLM 사용
llm = HuggingFaceHub(repo_id="google/flan-t5-base", model_kwargs={"temperature": 0.5})

# RAG 체인 생성
rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@router.post("/rag-search")
def rag_search(prompt: str = Body(..., embed=True)):
    response = rag_chain.run(prompt)
    return {"query": prompt, "response": response}
# OpenAI 기반 LLM 사용
llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

# RAG 체인 생성
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff"
)

@router.post("/rag-search")
def rag_search(prompt: str = Body(..., embed=True)):
    docs = retriever.get_relevant_documents(prompt)
    print("🔍 검색된 문서 수:", len(docs))
    for i, doc in enumerate(docs):
        print(f"[{i}] {doc.page_content[:100]}...")  # 일부 내용만 출력

    # chain.invoke는 dict 반환
    result = rag_chain.invoke({"query": prompt})
    
    return {
        "query": prompt,
        "result": result["result"] if isinstance(result, dict) and "result" in result else result
    }

@router.post("/rag-quest")
def rag_quest(input_data: QuestInput):
    result = generate_quest_with_rag(input_data)

    print("🧠 LLM 응답 결과:", result)

    try:
        parsed = json.loads(result)
        print("✅ JSON 파싱 성공:", parsed)

        # ✅ PostgreSQL에 저장
        db = next(get_session())
        log = QuestLog(
            user_id=input_data.user_id,
            goal=input_data.goal,
            main_category=input_data.main_category,
            sub_category=input_data.sub_category,
            quests=parsed["daily_quests"]
        )
        db.add(log)
        db.commit()

        # ✅ ChromaDB에도 저장
        vectorstore = load_chroma()
        doc_text = f"User {input_data.user_id} | Goal: {input_data.goal} | Category: {input_data.main_category}/{input_data.sub_category}\nGenerated Quests:\n{json.dumps(parsed['daily_quests'], ensure_ascii=False)}"
        doc = Document(page_content=doc_text)
        vectorstore.add_documents([doc])
        vectorstore.persist()

        return parsed

    except Exception as e:
        print("❌ 에러 발생:", e)
        return {
            "error": "LLM 응답을 JSON으로 파싱하거나 DB 저장 중 오류 발생",
            "detail": str(e),
            "raw_result": result
        }
    
@router.get("/quest-search-log/{user_id}")
def get_quest_log(user_id: str):
    db = next(get_session()) # DB 세션 열기
    logs = db.query(QuestLog).filter(QuestLog.user_id == user_id).all() # DB에서 유저 ID로 필터링하여 로그 검색 
    if not logs:
        raise HTTPException(status_code=404, detail="해당 유저의 퀘스트 로그가 없습니다.")
    return [
        {
            "id": log.id,
            "user_id": log.user_id,
            "goal": log.goal,
            "main_category": log.main_category,
            "sub_category": log.sub_category,
            "quests": log.quests
        }
        for log in logs
    ]
# 패키지 설치 안내
print("해당 패키지를 설치하려면 'requirements.txt'에 다음 라인을 추가하세요: langchain-huggingface")
