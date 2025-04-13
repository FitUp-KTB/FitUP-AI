from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import Session, sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()

POSTGRES_CONFIG = {
    "drivername": "postgresql+psycopg2",
    "username": os.getenv("PG_USER"),
    "password": os.getenv("PG_PASSWORD"),
    "host": os.getenv("PG_HOST"),
    "port": os.getenv("PG_PORT"),
    "database": os.getenv("PG_DB")
}

connect_args = {
    "sslmode": "verify-full",
    "sslrootcert": "aiven_ca/ca.pem"
}
# DB 연결을 위한 SSL 인증서 경로  -> 서버에 접속할 때 필요

engine = create_engine(URL.create(**POSTGRES_CONFIG), connect_args=connect_args)
# DB 연결을 위한 SQLAlchemy 엔진을 생성
# engine은 외부에서 import 하여 사용하면 됨
    # 예시: from DB.postgres_connector import engine

# DB 연결을 위한 SQLAlchemy 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_session() -> Session:
    db = SessionLocal()  # 세션 하나 생성 (창구 하나 열기)
    try:
        yield db
    finally:
        db.close()