"""
Exa Search MCP 통합 테스트
Plant Orchestrator와 새로운 Exa Search MCP 도구들의 연동 테스트
"""

import asyncio
import sys
from plant_orchestrator import PlantOrchestrator

async def test_exa_search_integration():
    """Exa Search MCP 통합 테스트"""
    
    print("🚀 Exa Search MCP 통합 테스트 시작")
    print("=" * 60)
    
    # Plant Orchestrator 초기화
    orchestrator = PlantOrchestrator()
    
    # 테스트 케이스들
    test_cases = [
        {
            "query": "몬스테라 키우는 방법 알려줘",
            "expected_tool": "web_search",
            "description": "기본 식물 관리 질문 - Exa Search 도구 자동 선택 테스트"
        },
        {
            "query": "2024년 최신 식물 트렌드는?",
            "expected_tool": "web_search", 
            "description": "트렌드 질문 - web_search_exa 도구 선택 예상"
        },
        {
            "query": "식물 관련 최신 연구 결과",
            "expected_tool": "web_search",
            "description": "연구 관련 질문 - research_paper_search_exa 도구 선택 예상"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📋 테스트 케이스 {i}/3")
        print(f"질문: {test_case['query']}")
        print(f"설명: {test_case['description']}")
        print("-" * 40)
        
        try:
            # Plant Orchestrator 실행
            result = orchestrator.analyze_and_execute(test_case['query'])
            
            # 결과 분석
            if result.get('success', False):
                print("✅ 오케스트레이터 실행 성공")
                
                # 웹 검색 도구가 사용되었는지 확인
                tools_used = result['query_analysis']['tools_needed']
                if 'web_search' in tools_used:
                    print("✅ Exa Search MCP 도구 선택됨")
                    
                    # 웹 검색 결과 확인
                    web_result = result['tool_results'].get('web_search', {})
                    if web_result:
                        print(f"🔍 검색 엔진: {web_result.get('search_engine', 'Unknown')}")
                        print(f"📊 검색 결과 수: {web_result.get('total_results', 0)}")
                        
                        used_exa_tools = web_result.get('used_tools', [])
                        if used_exa_tools and 'fallback' not in used_exa_tools:
                            print(f"🛠️  사용된 Exa 도구: {', '.join(used_exa_tools)}")
                            print("✅ MCP 연결 성공")
                        else:
                            print("⚠️  MCP 연결 실패 - Fallback 사용")
                        
                        summary = web_result.get('summary', '')
                        if summary:
                            print(f"📝 검색 요약: {summary[:100]}...")
                    else:
                        print("❌ 웹 검색 결과 없음")
                else:
                    print("❌ Exa Search 도구가 선택되지 않음")
                    
                print(f"🧠 AI 추론 과정: {result.get('reasoning', '')}")
                
            else:
                print(f"❌ 오케스트레이터 실행 실패: {result.get('reasoning', '')}")
                
        except Exception as e:
            print(f"💥 테스트 중 오류 발생: {str(e)}")
            import traceback
            print("🔍 상세 오류:")
            print(traceback.format_exc())
    
    print("\n" + "=" * 60)
    print("🏁 Exa Search MCP 통합 테스트 완료")

def main():
    """메인 실행 함수"""
    print("🔧 Exa Search MCP + Plant Orchestrator 통합 테스트")
    print("이 테스트는 다음을 확인합니다:")
    print("1. Plant Orchestrator가 웹 검색 도구를 올바르게 선택하는가?")
    print("2. Exa Search MCP 서버와 연결이 성공하는가?") 
    print("3. AI Agent가 적절한 Exa Search 도구를 선택하는가?")
    print("4. 검색 결과가 올바르게 반환되는가?")
    
    # Windows 비동기 정책 설정
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # 테스트 실행
    asyncio.run(test_exa_search_integration())

if __name__ == "__main__":
    main() 