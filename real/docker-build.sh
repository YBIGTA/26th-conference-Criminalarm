#!/bin/bash

echo "🐳 식물 친구 AI 도커 이미지 빌드 시작..."

# 이미지 빌드
docker build -t plant-friend-ai:latest .

if [ $? -eq 0 ]; then
    echo "✅ 도커 이미지 빌드 완료!"
    echo "📦 이미지 이름: plant-friend-ai:latest"
    
    # 이미지 정보 출력
    echo ""
    echo "🔍 빌드된 이미지 정보:"
    docker images plant-friend-ai:latest
    
    echo ""
    echo "🚀 실행 방법:"
    echo "1. 직접 실행: docker run -p 8000:8000 -e OPENAI_API_KEY=your_key plant-friend-ai:latest"
    echo "2. Docker Compose: docker-compose up"
else
    echo "❌ 도커 이미지 빌드 실패!"
    exit 1
fi 