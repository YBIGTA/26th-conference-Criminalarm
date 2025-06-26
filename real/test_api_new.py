#!/usr/bin/env python3

import requests
import json

def test_new_api():
    """새로운 API 방식 테스트 (data 폴더 제거 후)"""
    url = "http://localhost:8000/chat"
    
    print("🧪 새로운 API 방식 테스트 (data 폴더 제거)")
    print("=" * 60)
    
    # 테스트 1: 식물 데이터 + 일반 질문
    print("\n🔍 테스트 1: 식물 데이터 + 일반 질문")
    payload1 = {
        "message": "안녕 식물 트렌드 2024 5개 알려줘",
        "temperature": 25.5,
        "humidity": 60.0,
        "light_intensity": 800.0,
        "soil_moisture": 45.0
    }
    
    try:
        response1 = requests.post(url, json=payload1)
        print(f"상태 코드: {response1.status_code}")
        result1 = response1.json()
        print(f"성공: {result1['success']}")
        print(f"메시지 길이: {len(result1['message'])}")
        print(f"메시지: {result1['message'][:200]}...")
        
        if result1['plant_analysis']:
            pa = result1['plant_analysis']
            print(f"\n🌱 식물 분석:")
            print(f"  온도 상태: {pa['temperature_status']}")
            print(f"  습도 상태: {pa['humidity_status']}")
            print(f"  광도 상태: {pa['light_intensity_status']}")
            print(f"  토양 상태: {pa['soil_moisture_status']}")
            print(f"  건강도: {pa['overall_health_score']}점")
            print(f"  추천사항: {pa['recommendations']}")
        
    except Exception as e:
        print(f"테스트 1 실패: {e}")
    
    # 테스트 2: 식물 데이터 + 식물 상태 질문
    print("\n" + "=" * 60)
    print("🔍 테스트 2: 식물 데이터 + 식물 상태 질문")
    payload2 = {
        "message": "내 식물 상태가 어때?",
        "temperature": 30.0,  # 높은 온도
        "humidity": 25.0,     # 낮은 습도
        "light_intensity": 100.0,  # 낮은 광도
        "soil_moisture": 15.0  # 낮은 토양수분
    }
    
    try:
        response2 = requests.post(url, json=payload2)
        print(f"상태 코드: {response2.status_code}")
        result2 = response2.json()
        print(f"성공: {result2['success']}")
        print(f"메시지: {result2['message'][:300]}...")
        
        if result2['plant_analysis']:
            pa = result2['plant_analysis']
            print(f"\n🌱 식물 분석 (문제 상황):")
            print(f"  온도 상태: {pa['temperature_status']}")
            print(f"  습도 상태: {pa['humidity_status']}")
            print(f"  광도 상태: {pa['light_intensity_status']}")
            print(f"  토양 상태: {pa['soil_moisture_status']}")
            print(f"  건강도: {pa['overall_health_score']}점")
            print(f"  추천사항: {pa['recommendations']}")
        
    except Exception as e:
        print(f"테스트 2 실패: {e}")
    
    # 테스트 3: 부분 데이터만 있는 경우
    print("\n" + "=" * 60)
    print("🔍 테스트 3: 부분 데이터만 있는 경우")
    payload3 = {
        "message": "온도만 측정됐는데 어때?",
        "temperature": 22.0
        # 다른 데이터는 없음
    }
    
    try:
        response3 = requests.post(url, json=payload3)
        print(f"상태 코드: {response3.status_code}")
        result3 = response3.json()
        print(f"성공: {result3['success']}")
        print(f"메시지: {result3['message'][:300]}...")
        
        if result3['plant_analysis']:
            pa = result3['plant_analysis']
            print(f"\n🌱 식물 분석 (부분 데이터):")
            print(f"  온도 상태: {pa['temperature_status']}")
            print(f"  습도 상태: {pa['humidity_status']}")
            print(f"  광도 상태: {pa['light_intensity_status']}")
            print(f"  토양 상태: {pa['soil_moisture_status']}")
            print(f"  건강도: {pa['overall_health_score']}점")
        
    except Exception as e:
        print(f"테스트 3 실패: {e}")
    
    # 테스트 4: 식물 데이터 없음
    print("\n" + "=" * 60)
    print("🔍 테스트 4: 식물 데이터 없음")
    payload4 = {
        "message": "안녕하세요!"
    }
    
    try:
        response4 = requests.post(url, json=payload4)
        print(f"상태 코드: {response4.status_code}")
        result4 = response4.json()
        print(f"성공: {result4['success']}")
        print(f"메시지: {result4['message']}")
        print(f"식물 분석 있음: {result4['plant_analysis'] is not None}")
        
    except Exception as e:
        print(f"테스트 4 실패: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 모든 테스트 완료!")
    print("📝 결과 요약:")
    print("  - data 폴더 제거 완료")
    print("  - API 방식으로 식물 데이터 처리")
    print("  - 부분 데이터 및 데이터 없는 경우 처리")
    print("  - 식물 상태 분석 및 추천사항 제공")

if __name__ == "__main__":
    test_new_api() 