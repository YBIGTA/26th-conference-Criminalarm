from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any
import logging
import uvicorn
import os
import re

# ChatAgent 클래스 import
from chat_agent import ChatAgent
from tools.data_analyzer import EnvironmentDataAnalyzer

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="식물 친구 AI API",
    description="식물 관리 AI 챗봇 API",
    version="1.0.0"
)

# 전역 변수로 AI 시스템 초기화
chat_agent = None
data_analyzer = None

def initialize_chat_agent():
    """ChatAgent 초기화"""
    global chat_agent, data_analyzer
    try:
        logger.info("🌱 식물 친구 AI 시스템 초기화 중...")
        chat_agent = ChatAgent()
        data_analyzer = EnvironmentDataAnalyzer()
        logger.info("✅ AI 시스템 초기화 완료!")
        return True
    except Exception as e:
        logger.error(f"❌ AI 시스템 초기화 실패: {e}")
        return False

# 요청/응답 모델 정의
class ChatRequest(BaseModel):
    message: str
    temperature: Optional[float] = None
    light_intensity: Optional[float] = None
    soil_moisture: Optional[float] = None

class PlantAnalysisResult(BaseModel):
    temperature_status: str
    humidity_status: str
    light_intensity_status: str
    soil_moisture_status: str
    overall_health_score: int
    recommendations: list[str]

class ChatResponse(BaseModel):
    success: bool
    message: str
    plant_analysis: Optional[PlantAnalysisResult] = None
    error: Optional[str] = None

def parse_plant_analysis_from_api(plant_data: Dict, data_analyzer) -> PlantAnalysisResult:
    """API 데이터를 사용한 식물 분석 결과 생성"""
    try:
        # 새로운 API 방식으로 분석
        analysis = data_analyzer.analyze_plant_health_from_api(plant_data)
        
        # 개별 상태 확인
        temp_status = data_analyzer.get_status_for_api_response('temperature', plant_data.get('temperature'))
        light_status = data_analyzer.get_status_for_api_response('light_intensity', plant_data.get('light_intensity'))
        soil_status = data_analyzer.get_status_for_api_response('soil_moisture', plant_data.get('soil_moisture'))
        
        # 추천사항 가져오기
        recommendations = data_analyzer.get_recommendations_from_api(plant_data)
        
        result = PlantAnalysisResult(
            temperature_status=temp_status,
            humidity_status="정보 없음",
            light_intensity_status=light_status,
            soil_moisture_status=soil_status,
            overall_health_score=int(analysis.get('health_score', 50)),
            recommendations=recommendations
        )
        
        return result
        
    except Exception as e:
        logger.error(f"API 식물 분석 파싱 오류: {e}")
        return PlantAnalysisResult(
            temperature_status="분석 실패",
            humidity_status="분석 실패",
            light_intensity_status="분석 실패", 
            soil_moisture_status="분석 실패",
            overall_health_score=0,
            recommendations=["API 분석 중 오류가 발생했습니다"]
        )

def parse_plant_analysis(llm_response: str) -> PlantAnalysisResult:
    """LLM 응답에서 구조화된 식물 분석 결과 추출"""
    try:
        # 기본값 설정
        result = PlantAnalysisResult(
            temperature_status="정보 없음",
            humidity_status="정보 없음", 
            light_intensity_status="정보 없음",
            soil_moisture_status="정보 없음",
            overall_health_score=50,
            recommendations=["LLM 응답을 확인해주세요"]
        )
        
        # 점수 추출 (100점 만점에서 XX점 형태)
        score_match = re.search(r'(\d+)점', llm_response)
        if score_match:
            result.overall_health_score = int(score_match.group(1))
        
        # 상태 추출 (간단한 키워드 기반)
        if "온도" in llm_response:
            if any(word in llm_response for word in ["좋", "완벽", "적절"]):
                result.temperature_status = "좋음"
            elif any(word in llm_response for word in ["나쁨", "위험", "문제"]):
                result.temperature_status = "나쁨"
            else:
                result.temperature_status = "보통"
        
        if "광도" in llm_response or "빛" in llm_response:
            if any(word in llm_response for word in ["좋", "완벽", "적절"]):
                result.light_intensity_status = "좋음"
            elif any(word in llm_response for word in ["나쁨", "위험", "문제"]):
                result.light_intensity_status = "나쁨"
            else:
                result.light_intensity_status = "보통"
        
        if "토양" in llm_response or "수분" in llm_response:
            if any(word in llm_response for word in ["좋", "완벽", "적절"]):
                result.soil_moisture_status = "좋음"
            elif any(word in llm_response for word in ["나쁨", "위험", "문제"]):
                result.soil_moisture_status = "나쁨"
            else:
                result.soil_moisture_status = "보통"
        
        # 추천사항 추출 (간단하게 문장 단위로)
        recommendations = []
        lines = llm_response.split('\n')
        for line in lines:
            if any(keyword in line for keyword in ["추천", "조언", "권장", "해주세요", "하세요"]):
                clean_line = line.strip('- ').strip()
                if clean_line and len(clean_line) > 10:
                    recommendations.append(clean_line)
        
        if recommendations:
            result.recommendations = recommendations[:3]  # 최대 3개
        
        return result
        
    except Exception as e:
        logger.error(f"식물 분석 파싱 오류: {e}")
        return PlantAnalysisResult(
            temperature_status="분석 실패",
            humidity_status="분석 실패",
            light_intensity_status="분석 실패", 
            soil_moisture_status="분석 실패",
            overall_health_score=0,
            recommendations=["분석 중 오류가 발생했습니다"]
        )

@app.get("/")
async def root():
    """루트 엔드포인트"""
    return {
        "message": "🌱 식물 친구 AI API 서버가 실행 중입니다!",
        "endpoints": {
            "chat": "POST /chat - 채팅 및 식물 데이터 분석",
            "health": "GET /health - 서버 상태 확인"
        }
    }

@app.get("/health")
async def health_check():
    """헬스 체크 엔드포인트"""
    global chat_agent
    if chat_agent is None:
        initialize_chat_agent()
    
    return {
        "status": "healthy",
        "message": "식물 친구 AI가 건강하게 실행 중입니다! 🌱",
        "ai_initialized": chat_agent is not None
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """통합 채팅 엔드포인트 - 일반 채팅 및 식물 데이터 분석"""
    global chat_agent, data_analyzer
    
    try:
        logger.info(f"💬 요청: {request.message[:50]}...")
        
        # 시스템 초기화 (필요한 경우)
        if chat_agent is None or data_analyzer is None:
            if not initialize_chat_agent():
                raise HTTPException(
                    status_code=500, 
                    detail="AI 시스템 초기화에 실패했습니다."
                )
        
        # 사용자 입력 처리
        user_message = request.message.strip()
        if not user_message:
            return ChatResponse(
                success=False,
                message="메시지를 입력해주세요! 😊",
                error="Empty message"
            )
        
        # 식물 데이터가 있는지 확인
        has_plant_data = any([
            request.temperature is not None,
            request.light_intensity is not None,
            request.soil_moisture is not None
        ])
        
        # 사용자 질문이 식물 상태 관련인지 판단
        def is_plant_status_question(message: str) -> bool:
            plant_status_keywords = [
                "상태", "건강", "어때", "괜찮", "문제", "분석", "체크", "진단",
                "온도", "광도", "수분", "토양", "환경", "관리"
            ]
            return any(keyword in message.lower() for keyword in plant_status_keywords)
        
        plant_status_related = is_plant_status_question(user_message)
        
        if has_plant_data:
            logger.info("🌱 식물 데이터가 있음 - 분석 실행")
            
            # 현재 환경 데이터 구성
            current_data = {}
            if request.temperature is not None:
                current_data['temperature'] = request.temperature
            if request.light_intensity is not None:
                current_data['light_intensity'] = request.light_intensity
            if request.soil_moisture is not None:
                current_data['soil_moisture'] = request.soil_moisture
            
            # API 방식으로 변경 - 없는 데이터는 None으로 설정
            for key in ['temperature', 'light_intensity', 'soil_moisture']:
                if key not in current_data:
                    current_data[key] = None
            
            # 식물 분석 실행 (항상)
            analysis_prompt = f"""
당신은 식물 전문가입니다. 다음 환경 데이터를 분석하여 식물의 건강 상태를 평가해주세요.

현재 환경 데이터:
- 온도: {current_data.get('temperature', '정보 없음')}°C
- 광도: {current_data.get('light_intensity', '정보 없음')} lux
- 토양 수분: {current_data.get('soil_moisture', '정보 없음')}%

다음 사항을 포함하여 친근하고 상세한 분석을 제공해주세요:
1. 현재 환경 상태의 전반적인 평가
2. 각 환경 요소별 상태 (좋음/보통/나쁨)
3. 문제가 있다면 구체적인 개선 방법
4. 식물 관리 팁과 조언
5. 전체적인 건강도 점수 (100점 만점)

식물의 입장에서 친근하게 답변해주세요. 이모지를 적절히 사용하고, 실용적인 조언을 제공해주세요.
"""
            
            # 식물 분석 실행 (새로운 API 방식)
            if chat_agent is not None and data_analyzer is not None:
                analysis_response = chat_agent.chat(analysis_prompt, current_data)
                plant_analysis = parse_plant_analysis_from_api(current_data, data_analyzer)
            else:
                raise HTTPException(status_code=500, detail="AI 시스템이 초기화되지 않았습니다.")
            
            # 메시지 응답 처리
            if plant_status_related:
                logger.info("📋 식물 상태 질문 - 분석 결과 반환")
                user_response = analysis_response
            else:
                logger.info("💬 일반 질문 - 질문에만 답변 (환경 데이터 포함)")
                if chat_agent is not None:
                    user_response = chat_agent.chat(user_message, current_data)
                else:
                    raise HTTPException(status_code=500, detail="AI 시스템이 초기화되지 않았습니다.")
            
            logger.info("✅ 식물 데이터 분석 완료!")
            
            return ChatResponse(
                success=True,
                message=user_response,
                plant_analysis=plant_analysis
            )
            
        else:
            logger.info("💬 일반 채팅 모드")
            
            if chat_agent is not None:
                response = chat_agent.chat(user_message)
            else:
                raise HTTPException(status_code=500, detail="AI 시스템이 초기화되지 않았습니다.")
            
            logger.info("✅ 일반 채팅 처리 완료!")
            
            return ChatResponse(
                success=True,
                message=response
            )
        
    except Exception as e:
        logger.error(f"❌ 처리 중 오류: {e}")
        return ChatResponse(
            success=False,
            message="죄송해요, 처리 중에 문제가 생겼어요. 다시 시도해주세요! 😅",
            error=str(e)
        )

if __name__ == "__main__":
    # 환경 변수에서 설정 읽기
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print("🚀 식물 친구 AI API 서버 시작!")
    print(f"💬 통합 채팅: POST http://{host}:{port}/chat")
    print(f"🏥 헬스체크: GET http://{host}:{port}/health")
    print(f"📝 API 문서: http://{host}:{port}/docs")
    
    # AI 시스템 미리 초기화
    initialize_chat_agent()
    
    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    ) 