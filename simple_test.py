#!/usr/bin/env python3
"""
간단한 Orchestrator 테스트
"""

import os
import sys

# OpenAI API 키 설정 (더미)
os.environ["OPENAI_API_KEY"] = "sk-dummy-key-for-testing"

try:
    from plant_orchestrator import PlantOrchestrator
    from persona import PlantPersona
    
    print("🌱 모듈 임포트 성공!")
    
    # Orchestrator 초기화 테스트
    print("🤖 Orchestrator 초기화 중...")
    orchestrator = PlantOrchestrator()
    print("✅ Orchestrator 초기화 성공!")
    
    # Persona 초기화 테스트
    print("🎭 Persona 초기화 중...")
    persona = PlantPersona()
    print("✅ Persona 초기화 성공!")
    
    # 간단한 쿼리 테스트
    print("\n💬 간단한 쿼리 테스트...")
    test_query = "안녕하세요!"
    
    print(f"📤 쿼리: {test_query}")
    
    try:
        result = orchestrator.analyze_and_execute(test_query)
        print(f"✅ Orchestrator 결과: {result['success']}")
        print(f"🔧 사용된 도구: {result.get('query_analysis', {}).get('tools_needed', [])}")
        print(f"💭 추론: {result.get('reasoning', '')[:100]}...")
        
        # Persona 테스트
        persona_response = persona.generate_response(
            user_message=test_query,
            context=result.get('reasoning', ''),
            tools_data=result.get('tool_results', {})
        )
        print(f"🎭 Persona 응답: {persona_response[:100]}...")
        
    except Exception as e:
        print(f"❌ 쿼리 처리 중 오류: {e}")
        import traceback
        traceback.print_exc()
    
except Exception as e:
    print(f"❌ 초기화 중 오류: {e}")
    import traceback
    traceback.print_exc() 