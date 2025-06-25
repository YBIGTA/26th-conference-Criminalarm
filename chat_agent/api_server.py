from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import logging

# ChatAgent 클래스 import (기존 잘 작동하는 코드)
from chat_agent import ChatAgent

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="식물 친구 AI API",
    description="식물 관리 AI 챗봇 API",
    version="1.0.0"
)

# CORS 설정 (프론트엔드에서 접근 가능하도록)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 실제 운영시에는 특정 도메인만 허용
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 변수로 AI 시스템 초기화
chat_agent = None

@app.on_event("startup")
async def startup_event():
    """서버 시작시 AI 시스템 초기화"""
    global chat_agent
    try:
        logger.info("🌱 식물 친구 AI 시스템 초기화 중...")
        chat_agent = ChatAgent()
        logger.info("✅ AI 시스템 초기화 완료!")
    except Exception as e:
        logger.error(f"❌ AI 시스템 초기화 실패: {e}")
        raise

# 요청/응답 모델 정의
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    success: bool
    response: str
    error: Optional[str] = None

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "🌱 식물 친구 AI API 서버가 실행 중입니다!",
        "endpoints": {
            "chat": "POST /chat - 채팅 메시지 전송",
            "health": "GET /health - 서버 상태 확인"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    return {
        "status": "healthy",
        "message": "식물 친구 AI가 건강하게 실행 중입니다! 🌱"
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """메인 채팅 엔드포인트 - 입력받고 응답 반환"""
    try:
        logger.info(f"💬 채팅 요청: {request.message[:50]}...")
        
        if not chat_agent:
            raise HTTPException(
                status_code=500, 
                detail="AI 시스템이 초기화되지 않았습니다."
            )
        
        # 사용자 입력 처리
        user_message = request.message.strip()
        if not user_message:
            return ChatResponse(
                success=False,
                response="메시지를 입력해주세요! 😊",
                error="Empty message"
            )
        
        # ChatAgent로 처리 (기존 잘 작동하는 코드)
        response = chat_agent.chat(user_message)
        
        logger.info("✅ 채팅 처리 완료!")
        
        return ChatResponse(
            success=True,
            response=response
        )
        
    except Exception as e:
        logger.error(f"❌ 채팅 처리 중 오류: {e}")
        return ChatResponse(
            success=False,
            response="죄송해요, 처리 중에 문제가 생겼어요. 다시 시도해주세요! 😅",
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    import os
    
    # 환경 변수에서 설정 읽기
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print("🚀 식물 친구 AI API 서버 시작!")
    print(f"💬 채팅 엔드포인트: POST http://{host}:{port}/chat")
    print(f"🏥 헬스체크: GET http://{host}:{port}/health")
    print(f"📝 API 문서: http://{host}:{port}/docs")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    ) 