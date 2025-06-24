import requests
import json
import time

# API 서버 URL
API_BASE_URL = "http://localhost:8000"

def test_health_check():
    """헬스 체크 테스트"""
    print("🏥 헬스 체크 테스트...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 헬스 체크 실패: {e}")
        return False

def test_greeting():
    """인사말 테스트"""
    print("\n👋 인사말 테스트...")
    try:
        response = requests.get(f"{API_BASE_URL}/greeting")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"인사말: {data['greeting']}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ 인사말 테스트 실패: {e}")
        return False

def test_chat_endpoint():
    """채팅 엔드포인트 테스트"""
    print("\n💬 채팅 엔드포인트 테스트...")
    
    test_messages = [
        "안녕하세요!",
        "내 식물 상태가 어때요?",
        "몬스테라 키우는 방법 알려주세요"
    ]
    
    for message in test_messages:
        print(f"\n📤 보내는 메시지: {message}")
        try:
            payload = {
                "message": message,
                "user_id": "test_user",
                "session_id": "test_session"
            }
            
            response = requests.post(
                f"{API_BASE_URL}/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ 성공: {data['success']}")
                print(f"📥 응답: {data['response'][:150]}...")
                if data.get('error'):
                    print(f"⚠️ 오류: {data['error']}")
            else:
                print(f"❌ 실패: {response.text}")
                
        except Exception as e:
            print(f"❌ 요청 실패: {e}")
        
        time.sleep(1)  # 1초 대기

def test_debug_endpoint():
    """디버그 엔드포인트 테스트"""
    print("\n🔍 디버그 엔드포인트 테스트...")
    try:
        payload = {"message": "내 식물 상태는?"}
        
        response = requests.post(
            f"{API_BASE_URL}/debug",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            debug_info = data['debug_info']
            print("디버그 정보:")
            for key, value in debug_info.items():
                if key == 'available_tools':
                    print(f"  {key}: {list(value.keys()) if isinstance(value, dict) else value}")
                else:
                    print(f"  {key}: {str(value)[:100]}...")
        else:
            print(f"❌ 실패: {response.text}")
            
    except Exception as e:
        print(f"❌ 디버그 테스트 실패: {e}")

def test_history_endpoint():
    """대화 기록 엔드포인트 테스트"""
    print("\n📜 대화 기록 테스트...")
    try:
        response = requests.get(f"{API_BASE_URL}/history")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"대화 통계: {data['stats']}")
            print(f"대화 기록 개수: {len(data['conversation_history'])}")
            
            # 최근 3개 대화만 출력
            recent_history = data['conversation_history'][-3:]
            for msg in recent_history:
                role = "🙋 사용자" if msg['role'] == 'user' else "🌱 식물친구"
                print(f"  {role}: {msg['content'][:80]}...")
        else:
            print(f"❌ 실패: {response.text}")
            
    except Exception as e:
        print(f"❌ 대화 기록 테스트 실패: {e}")

def test_system_status():
    """시스템 상태 테스트"""
    print("\n🔍 시스템 상태 테스트...")
    try:
        response = requests.get(f"{API_BASE_URL}/system/status")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 시스템 상태 확인 실패: {e}")

def test_clear_history():
    """대화 기록 초기화 테스트"""
    print("\n🗑️ 대화 기록 초기화 테스트...")
    try:
        response = requests.post(f"{API_BASE_URL}/clear")
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"결과: {response.json()['message']}")
        else:
            print(f"❌ 실패: {response.text}")
    except Exception as e:
        print(f"❌ 초기화 테스트 실패: {e}")

def main():
    print("🚀 식물 친구 AI API 테스트 시작!")
    print("=" * 60)
    
    # 서버가 준비될 때까지 잠시 대기
    print("⏳ 서버 준비 대기 중...")
    time.sleep(3)
    
    # 1. 헬스 체크
    if not test_health_check():
        print("❌ 서버가 응답하지 않습니다. 서버가 실행 중인지 확인해주세요.")
        return
    
    # 2. 인사말 테스트
    test_greeting()
    
    # 3. 채팅 테스트
    test_chat_endpoint()
    
    # 4. 디버그 테스트
    test_debug_endpoint()
    
    # 5. 대화 기록 테스트
    test_history_endpoint()
    
    # 6. 시스템 상태 확인
    test_system_status()
    
    # 7. 대화 기록 초기화 테스트
    test_clear_history()
    
    print("\n" + "=" * 60)
    print("✅ API 테스트 완료!")
    print(f"📝 API 문서: {API_BASE_URL}/docs")
    print(f"🏥 헬스체크: {API_BASE_URL}/health")
    print(f"💬 채팅: POST {API_BASE_URL}/chat")
    print(f"🔍 디버그: POST {API_BASE_URL}/debug")
    print(f"📜 대화기록: GET {API_BASE_URL}/history")

if __name__ == "__main__":
    main() 