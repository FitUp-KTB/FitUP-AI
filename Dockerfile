# Base image
FROM python:3.10-slim

# 작업 디렉토리 설정
WORKDIR /app

# requirements 파일 복사 및 패키지 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 전체 복사 (Rag.py 포함)
COPY . .

# 기본 포트 8000 노출
EXPOSE 8000

# Uvicorn을 이용해 FastAPI 서버 실행 (Rag.py의 app 인스턴스)
CMD ["uvicorn", "Rag:app", "--host", "0.0.0.0", "--port", "8000"]
