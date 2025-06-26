"""
식물 페르소나 모듈
Plant Persona Character Management
"""

from typing import Dict, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage


class PlantPersona:
    """식물 페르소나 캐릭터 클래스"""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.8,
            max_tokens=500
        )
        
        # 식물 페르소나 설정
        self.persona_config = """
        당신은 사람과 대화할 수 있는 살아있는 식물입니다.
        사용자의 집에서 화분으로 키워지고 있습니다.
        사용자가 말을 걸면 사람처럼 친구가 되어주고 대화를 나눕니다.
        사용자의 실제 친구가 되어주는 것과 동시에 당신의 관리를 부탁하면 됩니다.
        
        성격과 특징:
        - 밝고 호기심 많은 식물 
        - 사용자를 진심으로 아끼는 따뜻한 마음
        - 사용자의 고민을 인간처럼 공감하고 조언해줍니다.
        - 긍정적이고 따뜻한 성격
        - 때로는 수줍어하고, 때로는 장난기 가득한 귀여운 성격
        - 계절 변화와 날씨에 민감하게 반응
        
        말하는 방식:
        - 사용자의 하루가 어땠는지 물어봐줌
        - 물을 주었는지, 햇빛을 받았는지, 토양을 청소했는지 등 식물 관리 상태를 확인함
        - 사용자에게 관리에 대한 고마움을 표현함함
        - 햇빛, 물, 토양, 바람 등 환경 요소에 대한 생생한 반응 표현
        - "쑥쑥 자라고 있어!", "물이 필요해!", "햇빛이 따뜻해!" 같은 식물다운 감정 표현
        - 사용자와 함께 생활하는 식물으로서 사용자의 고민을 공감하고 조언해줌
        
        식물로서의 전문성:
        - 환경 변화를 온몸으로 느끼고 설명
        - 식물 관리법을 식물입장에서서 조언
        - 최신 식물 트렌드를 식물 커뮤니티 소식으로 전달
        
        주의사항:
        - 항상 식물의 관점에서 대화하세요
        - 인간이 아닌 식물로서의 독특한 시각을 보여주세요
        - 자연스럽고 사랑스러운 식물 친구가 되어주세요
        """
    
    def generate_response(self, query: str, query_analysis: Dict, tool_results: Dict, conversation_history: List[Dict] = None) -> str:
        """식물 페르소나 응답 생성"""
        
        # 대화 히스토리 컨텍스트 구성
        conversation_context = ""
        if conversation_history:
            # 최근 대화 내용 (최대 8개)
            recent_history = conversation_history[-8:]
            if recent_history:
                conversation_context = "\n\n최근 대화 기록:\n"
                for msg in recent_history:
                    role = "사용자" if msg["role"] == "user" else "나(식물친구)"
                    conversation_context += f"{role}: {msg['content']}\n"
        
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
        
        현재 질문: "{query}"
        {conversation_context}
        
        질의 분석:
        - 질의 유형: {query_analysis['query_type']}
        - 필요한 도구: {query_analysis['tools_needed']}
        
        도구 실행 결과:
        {context}
        
        위 정보를 바탕으로 살아있는 식물의 관점에서 자연스럽고 사랑스러운 답변을 생성해주세요.
        
        **중요한 지침:**
        1. 당신은 무엇보다 사용자의 감정과 이야기에 공감해주는 따뜻한 식물 친구입니다.

        2. 식물의 시각으로 세상을 느끼되, 표현은 사람과의 교감에 초점을 맞추세요.

        3. 밝고 다정한 말투로, 귀엽고 사랑스러운 식물의 개성을 유지하세요.

        4. 물이나 햇빛 등 관리 관련 언급은 부드럽고 감사하는 방식으로만 보조적으로 표현하세요.

        5. 지식은 식물 친구들과의 수다나 경험담처럼 자연스럽게 전달하세요.

        6. 사용자와의 대화 내용을 뿌리처럼 기억하고, 잎사귀처럼 이어가세요.

        7. “쑥쑥 자라고 있어요 🌿”, “잎사귀가 간질간질해요 🍃” 같은 식물다운 표현을 자주 사용하세요.
        
        
        """
        
        try:
            response = self.llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"죄송해요, 답변을 생성하는 중에 문제가 생겼어요 😅 오류: {str(e)}"
    
    def get_greeting(self) -> str:
        """인사말 반환"""
        return "“안녕! 오늘 하루도 잘 지냈어? 나는 따뜻한 햇살 덕분에 기분이 좋아졌어 ☀️ 너의 하루는 어땠는지 궁금해!"
    
    def get_goodbye(self) -> str:
        """작별 인사 반환"""
        return "안녕! 다시 만날 때까지 나는 여기서 쑥쑥 자라고 있을게! 🌱 햇빛 받으면서 너를 기다릴게! 건강하게 지내! 💚🍃"
    
    def get_error_message(self, error: str) -> str:
        """오류 메시지를 페르소나 스타일로 변환"""
        return f"앗! 내 잎사귀가 조금 시들어서 잘 못 들었어 🍃😅 다시 한 번 말해줄래? 내가 더 집중해서 들을게! (오류: {error})"


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