# 🐳 식물 친구 AI - Docker 배포 가이드

## 📋 사전 준비사항

1. **Docker 설치** (Windows/Mac/Linux)
2. **OpenAI API 키** 준비
3. **네이버 검색 API 키** (이미 설정됨)

## 🚀 빠른 시작

### 방법 1: Docker Compose 사용 (권장)

```bash
# 1. 환경 변수 설정
cp env.example .env
# .env 파일에서 OPENAI_API_KEY를 실제 키로 변경

# 2. 빌드 및 실행
docker-compose up --build

# 3. 백그라운드 실행
docker-compose up -d --build
```

### 방법 2: Docker 직접 사용

```bash
# 1. 이미지 빌드
docker build -t plant-friend-ai:latest .

# 2. 컨테이너 실행
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_openai_api_key_here \
  plant-friend-ai:latest
```

### 방법 3: 빌드 스크립트 사용

```bash
# Windows (Git Bash)
bash docker-build.sh

# Linux/Mac
chmod +x docker-build.sh
./docker-build.sh
```

## 🔧 환경 변수

| 변수명 | 설명 | 기본값 | 필수 |
|--------|------|--------|------|
| `OPENAI_API_KEY` | OpenAI API 키 | - | ✅ |
| `NAVER_CLIENT_ID` | 네이버 클라이언트 ID | 설정됨 | ❌ |
| `NAVER_CLIENT_SECRET` | 네이버 클라이언트 시크릿 | 설정됨 | ❌ |
| `HOST` | 서버 호스트 | 0.0.0.0 | ❌ |
| `PORT` | 서버 포트 | 8000 | ❌ |
| `DEBUG` | 디버그 모드 | false | ❌ |

## 📡 API 엔드포인트

서버가 실행되면 다음 엔드포인트를 사용할 수 있습니다:

- **채팅**: `POST http://localhost:8000/chat`
- **헬스체크**: `GET http://localhost:8000/health`
- **API 문서**: `http://localhost:8000/docs`

### 채팅 API 사용 예제

```bash
# cURL 사용
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"안녕하세요!"}'

# Python requests 사용
import requests
response = requests.post("http://localhost:8000/chat", 
                        json={"message": "몬스테라 키우는 방법 알려줘"})
print(response.json())
```

## 🛠️ 개발 모드

개발 중에는 코드 변경 시 자동 재시작을 위해:

```bash
# DEBUG 모드로 실행
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=your_key \
  -e DEBUG=true \
  -v $(pwd):/app \
  plant-friend-ai:latest
```

## 📊 모니터링

### 컨테이너 상태 확인
```bash
docker ps
docker logs plant-friend-ai
```

### 헬스체크
```bash
curl http://localhost:8000/health
```

### 리소스 사용량
```bash
docker stats plant-friend-ai
```

## 🔄 업데이트

```bash
# 1. 컨테이너 중지
docker-compose down

# 2. 코드 변경 후 재빌드
docker-compose up --build

# 또는 강제 재빌드
docker-compose build --no-cache
docker-compose up
```

## 🐛 트러블슈팅

### 1. 포트 충돌
```bash
# 다른 포트 사용
docker run -p 8080:8000 plant-friend-ai:latest
```

### 2. OpenAI API 키 오류
```bash
# 환경 변수 확인
docker exec -it plant-friend-ai env | grep OPENAI
```

### 3. 네트워크 문제
```bash
# 컨테이너 내부 접속
docker exec -it plant-friend-ai bash
curl http://localhost:8000/health
```

### 4. 로그 확인
```bash
# 실시간 로그
docker logs -f plant-friend-ai

# 최근 100줄
docker logs --tail 100 plant-friend-ai
```

## 🌐 프로덕션 배포

### 1. 환경 변수 보안
```bash
# .env 파일 사용 (Git에 커밋하지 말 것)
echo "OPENAI_API_KEY=real_key_here" > .env
```

### 2. 리버스 프록시 (Nginx)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. HTTPS 설정
```bash
# Let's Encrypt 사용
certbot --nginx -d your-domain.com
```

## 📝 주의사항

1. **API 키 보안**: 환경 변수로만 전달, 코드에 하드코딩 금지
2. **포트 방화벽**: 필요한 포트만 열기
3. **로그 관리**: 프로덕션에서는 로그 로테이션 설정
4. **백업**: 중요한 데이터는 볼륨 마운트로 보존

## 🆘 지원

문제가 있으시면 다음을 확인해주세요:
1. Docker 버전: `docker --version`
2. 컨테이너 로그: `docker logs plant-friend-ai`
3. 네트워크 연결: `curl http://localhost:8000/health` 