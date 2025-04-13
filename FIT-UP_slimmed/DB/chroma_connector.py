from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
# Chroma DB에 저장된 벡터를 불러오기 위한 임베딩 모델을 정의합니다.
# 이 모델은 문서의 의미를 벡터로 변환하는 데 사용됩니다.

def create_chroma_from_text(text_file_path: str = "docs/rag_samples.txt", persist_dir: str = "chroma_db"): # create_chroma_from_text()만 호출해도 자동으로 docs/rag_samples.txt 연결

    # 1. 텍스트 파일 로딩
    loader = TextLoader(text_file_path, encoding="utf-8")
    documents = loader.load()

    # 2. 문서 분할
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(documents)

    # 3. 벡터 저장
    vectordb = Chroma.from_documents(documents=split_docs, embedding=embedding, persist_directory=persist_dir)
    vectordb.persist()
    return vectordb

def load_chroma():
    return Chroma(persist_directory="chroma_db", embedding_function=embedding)
# 저장된 벡터를 로드합니다.
# persist_directory는 Chroma DB의 저장 경로를 지정
# 이 경로에서 벡터를 로드하여 검색 기능을 수행