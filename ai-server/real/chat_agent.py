"""
채팅 에이전트 모듈
Chat Agent for Conversation Management
"""

from typing import Dict, List
from persona import PlantPersona
from plant_orchestrator import PlantOrchestrator


class ChatAgent:
    """대화 전체를 관리하는 채팅 에이전트"""
    
    def __init__(self):
        """초기화"""
        self.persona = PlantPersona()
        self.orchestrator = PlantOrchestrator()
        self.conversation_history = []
    
    def chat(self, message: str) -> str:
        """메인 채팅 인터페이스"""
        try:
            # 대화 기록에 사용자 메시지 추가
            self.conversation_history.append({"role": "user", "content": message})
            
            # 1. LangGraph 기반 AI 분석 및 도구 실행
            orchestrator_result = self.orchestrator.analyze_and_execute(message)
            
            if not orchestrator_result["success"]:
                error_response = self.persona.get_error_message(orchestrator_result["reasoning"])
                self.conversation_history.append({"role": "assistant", "content": error_response})
                return error_response
            
            # 2. 페르소나 응답 생성
            response = self.persona.generate_response(
                message, 
                orchestrator_result["query_analysis"], 
                orchestrator_result["tool_results"]
            )
            
            # 대화 기록에 응답 추가
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            error_response = self.persona.get_error_message(str(e))
            self.conversation_history.append({"role": "assistant", "content": error_response})
            return error_response
    
    def get_conversation_history(self) -> List[Dict]:
        """대화 기록 반환"""
        return self.conversation_history.copy()
    
    def clear_history(self):
        """대화 기록 초기화"""
        self.conversation_history = []
    
    def get_greeting(self) -> str:
        """인사말 반환"""
        return self.persona.get_greeting()
    
    def get_goodbye(self) -> str:
        """작별 인사 반환"""
        return self.persona.get_goodbye()
    
    def get_debug_info(self, message: str) -> Dict:
        """디버깅용 정보 반환"""
        try:
            orchestrator_result = self.orchestrator.analyze_and_execute(message)
            
            return {
                "query_analysis": orchestrator_result["query_analysis"],
                "tool_results": orchestrator_result["tool_results"],
                "ai_reasoning": orchestrator_result["reasoning"],
                "success": orchestrator_result["success"],
                "conversation_length": len(self.conversation_history),
                "available_tools": self.orchestrator.get_available_tools()
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_stats(self) -> Dict:
        """대화 통계 반환"""
        if not self.conversation_history:
            return {"total_messages": 0, "user_messages": 0, "assistant_messages": 0}
        
        user_count = len([msg for msg in self.conversation_history if msg["role"] == "user"])
        assistant_count = len([msg for msg in self.conversation_history if msg["role"] == "assistant"])
        
        return {
            "total_messages": len(self.conversation_history),
            "user_messages": user_count,
            "assistant_messages": assistant_count
        }


# 터미널 채팅 인터페이스
def main():
    """터미널 채팅 인터페이스"""
    print("🌱 식물 친구 AI에 오신 걸 환영해요! 🌱")
    print("대화를 시작하려면 메시지를 입력하세요. 종료하려면 'quit'를 입력하세요.")
    print("-" * 50)
    
    # 채팅 에이전트 초기화
    try:
        chat_agent = ChatAgent()
        print("✅ 시스템 초기화 완료!")
        print(f"🌱 식물 친구: {chat_agent.get_greeting()}")
    except Exception as e:
        print(f"❌ 초기화 실패: {str(e)}")
        print("OpenAI API 키가 설정되었는지 확인해주세요.")
        return
    
    # 채팅 루프
    while True:
        try:
            user_input = input("\n🙋 사용자: ").strip()
            
            if user_input.lower() in ['quit', 'exit', '종료', '나가기']:
                print(f"🌱 식물 친구: {chat_agent.get_goodbye()}")
                break
            
            if not user_input:
                continue
            
            # 특별 명령어 처리
            if user_input.startswith("debug:"):
                query = user_input[6:].strip()
                debug_info = chat_agent.get_debug_info(query)
                print(f"\n🔍 디버그 정보:")
                for key, value in debug_info.items():
                    print(f"  {key}: {value}")
                continue
            
            if user_input.lower() in ['stats', '통계']:
                stats = chat_agent.get_stats()
                print(f"\n📊 대화 통계:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                continue
            
            if user_input.lower() in ['clear', '초기화']:
                chat_agent.clear_history()
                print("🗑️ 대화 기록이 초기화되었습니다.")
                continue
            
            # 일반 채팅
            print("🤔 생각 중...")
            response = chat_agent.chat(user_input)
            print(f"\n🌱 식물 친구: {response}")
            
        except KeyboardInterrupt:
            print(f"\n🌱 식물 친구: {chat_agent.get_goodbye()}")
            break
        except Exception as e:
            print(f"❌ 오류 발생: {str(e)}")


if __name__ == "__main__":
    main() 