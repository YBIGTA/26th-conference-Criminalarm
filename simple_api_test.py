import requests
import json

# API 서버 URL
API_BASE_URL = "http://localhost:8000"

def test_chat(message):
    """채팅 테스트"""
    try:
        payload = {"message": message}
        
        response = requests.post(
            f"{API_BASE_URL}/chat",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print(f"🌱 식물친구: {data['response']}")
            else:
                print(f"❌ 오류: {data.get('error', 'Unknown error')}")
        else:
            print(f"❌ HTTP 오류: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 요청 실패: {e}")

def main():
    print("🌱 식물 친구 AI 간단 테스트")
    print("=" * 40)
    
    # 헬스 체크
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ 서버 정상 작동")
        else:
            print("❌ 서버 문제")
            return
    except:
        print("❌ 서버에 연결할 수 없습니다.")
        return
    
    # 채팅 테스트
    test_messages = [
        "안녕하세요!",
        "내 식물 상태는 어때요?",
        "몬스테라 키우는 방법 알려주세요"
    ]
    
    for message in test_messages:
        print(f"\n🙋 사용자: {message}")
        test_chat(message)
    
    print("\n" + "=" * 40)
    print("✅ 테스트 완료!")

if __name__ == "__main__":
    main() 