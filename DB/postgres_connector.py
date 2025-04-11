from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
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

engine = create_engine(URL.create(**POSTGRES_CONFIG), connect_args=connect_args)

# engine은 외부에서 import 하여 사용하세요.
# 예: from DB.postgres_connector import engine