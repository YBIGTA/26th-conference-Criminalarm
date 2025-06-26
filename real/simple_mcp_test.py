"""
가장 간단한 MCP 연결 테스트
직접적인 MCP 서버 연결과 도구 확인
"""

import asyncio
import sys
import os

async def test_mcp_connection():
    """MCP 서버 연결 테스트"""
    
    print("🔧 MCP 연결 테스트 시작")
    print("=" * 50)
    
    try:
        # MCP 서버 설정 (config.py에서 가져오기)
        MCP_SERVERS = {
            "exa": {
                "command": "cmd",
                "args": [
                    "/c",
                    "npx",
                    "-y",
                    "@smithery/cli@latest",
                    "run",
                    "exa", 
                    "--key",
                    "d52a2502-98a5-452f-9ce7-65f507929073"
                ],
                "transport": "stdio"
            }
        }
        
        print("📦 MCP 어댑터 임포트 중...")
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        print("🔄 MCP 서버 연결 시도...")
        client = MultiServerMCPClient(MCP_SERVERS)
        
        print("🛠️  도구 목록 가져오는 중...")
        tools = await client.get_tools()
        
        if tools:
            print(f"✅ MCP 연결 성공! 도구 {len(tools)}개 발견:")
            for tool in tools:
                print(f"   - {tool.name}: {tool.description[:60]}...")
        else:
            print("❌ 도구를 찾을 수 없습니다.")
            
        return True
        
    except ImportError as e:
        print(f"❌ 패키지 임포트 실패: {str(e)}")
        print("💡 해결 방법: pip install langchain-mcp-adapters")
        return False
        
    except Exception as e:
        print(f"❌ MCP 연결 실패: {str(e)}")
        print("🔍 상세 오류:")
        import traceback
        print(traceback.format_exc())
        return False

async def test_simple_search():
    """간단한 검색 테스트"""
    
    print("\n🔍 간단한 검색 테스트")
    print("=" * 50)
    
    try:
        # OpenAI API 키 확인
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
        
        if OPENAI_API_KEY == "your_openai_api_key_here":
            print("❌ OpenAI API 키가 설정되지 않았습니다.")
            print("💡 해결 방법: Windows CMD에서 'set OPENAI_API_KEY=your_actual_key' 실행")
            return False
        
        print("🔑 OpenAI API 키 확인됨")
        
        # MCP 및 LangChain 임포트
        from langchain_mcp_adapters.client import MultiServerMCPClient
        from langgraph.prebuilt import create_react_agent
        from langchain_openai import ChatOpenAI
        
        # MCP 설정
        MCP_SERVERS = {
            "exa": {
                "command": "cmd", 
                "args": [
                    "/c",
                    "npx",
                    "-y", 
                    "@smithery/cli@latest",
                    "run",
                    "exa",
                    "--key",
                    "d52a2502-98a5-452f-9ce7-65f507929073"
                ],
                "transport": "stdio"
            }
        }
        
        print("🔄 MCP 클라이언트 연결 중...")
        client = MultiServerMCPClient(MCP_SERVERS)
        tools = await client.get_tools()
        
        print(f"🛠️  도구 {len(tools)}개 로드됨")
        
        print("🤖 OpenAI LLM 초기화 중...")
        llm = ChatOpenAI(
            api_key=OPENAI_API_KEY,
            model="gpt-3.5-turbo",
            temperature=0.1
        )
        
        print("🔗 LangGraph Agent 생성 중...")
        agent = create_react_agent(llm, tools)
        
        print("🔍 테스트 검색 실행 중...")
        test_query = "몬스테라 식물 정보"
        
        response = await agent.ainvoke({
            "messages": [{"role": "user", "content": f"Search for information about: {test_query}"}]
        })
        
        print("✅ 검색 완료!")
        
        # 사용된 도구 확인
        used_tools = []
        for message in response['messages']:
            if hasattr(message, 'tool_calls') and message.tool_calls:
                for tool_call in message.tool_calls:
                    used_tools.append(tool_call['name'])
        
        if used_tools:
            print(f"🛠️  사용된 도구: {', '.join(used_tools)}")
        else:
            print("⚠️  도구가 사용되지 않음")
            
        # 최종 답변
        final_answer = response['messages'][-1].content
        print(f"📝 답변 길이: {len(final_answer)} 문자")
        print(f"📄 답변 미리보기: {final_answer[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ 검색 테스트 실패: {str(e)}")
        import traceback
        print("🔍 상세 오류:")
        print(traceback.format_exc())
        return False

async def main():
    """메인 테스트 함수"""
    print("🚀 MCP Exa Search 연결 테스트")
    print("=" * 60)
    
    # 1단계: 기본 MCP 연결 테스트
    connection_success = await test_mcp_connection()
    
    if connection_success:
        # 2단계: 실제 검색 테스트
        search_success = await test_simple_search()
        
        if search_success:
            print("\n🎉 모든 테스트 통과! MCP 연결이 정상적으로 작동합니다.")
        else:
            print("\n⚠️  MCP 연결은 성공했지만 검색 테스트에서 문제 발생")
    else:
        print("\n❌ MCP 연결 실패")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    # Windows 비동기 정책 설정
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    # 테스트 실행
    asyncio.run(main()) 