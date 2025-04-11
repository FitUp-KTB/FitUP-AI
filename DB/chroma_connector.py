
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embedding = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def load_chroma():
    return Chroma(persist_directory="chroma_db", embedding_function=embedding)
