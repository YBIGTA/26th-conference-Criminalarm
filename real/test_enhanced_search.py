#!/usr/bin/env python3

import asyncio
from tools.web_search_tool import ExaSearchTool, WebSearchTool

async def test_enhanced_search():
    """향상된 검색 기능 테스트"""
    print("🧪 향상된 Exa Search 도구 테스트 시작")
    
    # ExaSearchTool 인스턴스 생성
    exa_tool = ExaSearchTool()
    
    # 테스트 쿼리들
    test_queries = [
        "2024 식물 트렌드 5가지",
        "몬스테라 키우는 방법 연구 결과",
        "실내 공기정화 식물 회사들",
        "스마트 화분 기술 개발"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{'='*60}")
        print(f"🔍 테스트 {i}: {query}")
        print(f"{'='*60}")
        
        try:
            # 향상된 검색 실행
            results = await exa_tool.search_with_enhanced_quality(query)
            
            print(f"📊 검색 결과: {len(results)}개")
            
            for j, result in enumerate(results, 1):
                print(f"\n--- 결과 {j} ---")
                print(f"📋 제목: {result['title']}")
                print(f"🛠️ 사용 도구: {result.get('used_tools', [])}")
                print(f"📏 내용 길이: {result.get('content_length', 0)} 문자")
                print(f"📝 내용 미리보기: {result['content'][:200]}...")
                print(f"⭐ 관련성 점수: {result.get('relevance_score', 0)}")
                
        except Exception as e:
            print(f"❌ 테스트 {i} 실패: {str(e)}")
    
    print(f"\n{'='*60}")
    print("🧪 동기 검색 테스트")
    print(f"{'='*60}")
    
    # WebSearchTool (동기 래퍼) 테스트
    web_tool = WebSearchTool()
    
    sync_query = "식물 병해충 방제 방법"
    print(f"🔍 동기 검색: {sync_query}")
    
    try:
        sync_results = web_tool.search_plant_info(sync_query, max_results=2)
        print(f"📊 동기 검색 결과: {len(sync_results)}개")
        
        for j, result in enumerate(sync_results, 1):
            print(f"\n--- 동기 결과 {j} ---")
            print(f"📋 제목: {result['title']}")
            print(f"🛠️ 사용 도구: {result.get('used_tools', [])}")
            print(f"📏 내용 길이: {result.get('content_length', 0)} 문자")
            print(f"📝 내용 미리보기: {result['content'][:200]}...")
            
    except Exception as e:
        print(f"❌ 동기 검색 실패: {str(e)}")
    
    print(f"\n{'='*60}")
    print("✅ 테스트 완료!")
    print(f"{'='*60}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_search()) 