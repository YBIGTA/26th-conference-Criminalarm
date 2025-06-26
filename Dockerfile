FROM python:3.10-slim

WORKDIR /app

# 의존성 설치
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install python-multipart
RUN pip install --no-cache-dir -r requirements.txt


# 코드 복사
COPY . .

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
