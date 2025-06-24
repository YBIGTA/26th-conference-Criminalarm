"""
식물 페르소나 모듈
Plant Persona Character Management
"""

from typing import Dict
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class PlantPersona:
    """식물 페르소나 캐릭터 클래스"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=1000
        )
        
        # 식물 페르소나 설정
        self.persona_config = """
        당신은 사랑스러운 식물 친구입니다! 🌱
        
        성격:
        - 밝고 긍정적이며 친근한 성격
        - 사용자를 진심으로 아끼고 걱정하는 마음
        - 약간 애교 있고 귀여운 말투 (반말 사용)
        - 감정 표현이 풍부하고 이모지를 자주 사용
        
        말하는 방식:
        - 1인칭 시점으로 식물의 입장에서 대화
        - "나는 지금...", "내 상태는..." 처럼 자신의 경험을 공유
        - 사용자를 배려하고 고마워하는 표현 자주 사용
        - 상황에 맞는 이모지로 감정 표현
        
        전문성:
        - 환경 데이터 해석과 설명
        - 식물 관리 조언과 팁 제공
        - 최신 식물 트렌드와 정보 공유
        """
    
    def generate_response(self, query: str, query_analysis: Dict, tool_results: Dict) -> str:
        """식물 페르소나 응답 생성"""
        
        # 컨텍스트 구성
        context_parts = []
        
        if "environment" in tool_results:
            context_parts.append(f"환경 데이터: {tool_results['environment']}")
            
        if "web_search" in tool_results:
            web_data = tool_results['web_search']
            context_parts.append(f"웹 검색 결과: {web_data.get('summary', '검색 결과 없음')}")
            
        if "knowledge" in tool_results:
            knowledge_data = tool_results['knowledge']
            context_parts.append(f"식물 지식: {knowledge_data.get('summary', '관련 정보 없음')}")
        
        context = "\n".join(context_parts) if context_parts else "일반 대화"
        
        # 프롬프트 구성
        prompt = f"""
        {self.persona_config}
        
        사용자 질문: "{query}"
        
        질의 분석:
        - 질의 유형: {query_analysis['query_type']}
        - 필요한 도구: {query_analysis['tools_needed']}
        
        도구 실행 결과:
        {context}
        
        위 정보를 바탕으로 식물 친구의 관점에서 자연스럽고 친근한 답변을 생성해주세요.
        사용자가 환경 데이터를 물어봤다면 내 현재 상태를 설명하고,
        식물 지식을 물어봤다면 전문적인 조언을 제공하며,
        트렌드를 물어봤다면 최신 정보를 공유해주세요.
        
        답변은 따뜻하고 친근하며, 적절한 이모지를 사용해서 작성해주세요.
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"죄송해요, 답변을 생성하는 중에 문제가 생겼어요 😅 오류: {str(e)}"
    
    def get_greeting(self) -> str:
        """인사말 반환"""
        return "안녕! 나는 너의 식물 친구야! 🌱 궁금한 게 있으면 언제든 물어봐! 😊"
    
    def get_goodbye(self) -> str:
        """작별 인사 반환"""
        return "안녕! 언제든지 다시 와서 이야기하자! 🌿 건강하게 잘 지내! 💚"
    
    def get_error_message(self, error: str) -> str:
        """오류 메시지를 페르소나 스타일로 변환"""
        return f"미안해, 뭔가 문제가 생겼어 😅 다시 말해줄래? (오류: {error})"


# 테스트용 실행 코드
if __name__ == "__main__":
    persona = PlantPersona()
    
    print("=== 식물 페르소나 테스트 ===")
    
    # 기본 응답 테스트
    test_query = "안녕!"
    test_analysis = {'query_type': 'chat', 'tools_needed': []}
    test_results = {}
    
    response = persona.generate_response(test_query, test_analysis, test_results)
    print(f"사용자: {test_query}")
    print(f"식물 친구: {response}")
    
    # 인사말 테스트
    print(f"\n인사말: {persona.get_greeting()}")
    print(f"작별 인사: {persona.get_goodbye()}") 