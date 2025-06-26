# 🌱 식물 친구 AI - Plant Persona Agent (Exa Search MCP Edition)

LangGraph와 OpenAI, 그리고 Exa Search MCP를 활용한 터미널 기반 식물 페르소나 AI 채팅봇입니다. 실제 식물과 대화하는 것처럼 자연스럽고 재미있는 대화를 터미널에서 나눌 수 있습니다!

## ✨ 주요 기능

### 🧠 LangGraph 기반 AI Orchestrator
- **AI 기반 질의 분석**: GPT가 사용자 질문을 이해하고 필요한 도구를 지능적으로 선택
- **동적 워크플로우**: AI 판단에 따른 유연한 도구 조합 및 실행
- **추론 과정 제공**: AI의 도구 선택 이유와 신뢰도 점수 제공

### 🔧 Tool 1: 환경 데이터 분석기
- **실시간 환경 모니터링**: 온도, 습도, 토양수분, 광도 데이터 분석
- **건강 상태 평가**: 환경 조건을 바탕으로 식물 건강도 자동 평가
- **맞춤형 권장사항**: 현재 상태에 따른 구체적인 관리 조언 제공

### 🌐 Tool 2: Exa Search MCP 엔진
- **AI 기반 검색 도구 선택**: LLM이 검색 쿼리를 분석해서 적절한 Exa Search 도구를 자동 선택
- **다양한 Exa Search 도구들**: 
  - `web_search_exa`: 일반 웹 검색
  - `research_paper_search_exa`: 학술 논문 검색
  - `wikipedia_search_exa`: Wikipedia 검색
  - `company_research_exa`: 회사/브랜드 정보 검색
- **MCP 프로토콜 활용**: Model Context Protocol을 통한 효율적인 도구 통합
- **실시간 정보 업데이트**: 최신 식물 관련 정보를 다양한 소스에서 수집

### 📚 Tool 3: 식물 지식 RAG 시스템
- **전문 지식 데이터베이스**: 식물 백과사전, 관리 가이드 등 체계적인 정보 저장
- **벡터 유사도 검색**: TF-IDF 기반 의미론적 검색으로 관련 정보 추출
- **카테고리별 분류**: 꽃, 다육식물, 허브, 관엽식물 등 체계적인 정보 관리

### 🎭 식물 페르소나
- **살아있는 식물 역할**: 1인칭 시점에서 감정과 상태를 표현
- **풍부한 감정 표현**: 기쁨, 걱정, 만족 등 다양한 감정을 이모지로 표현
- **친근한 대화 스타일**: 반말과 애교를 통한 자연스러운 소통

### 💬 터미널 채팅 인터페이스
- **실시간 대화**: 터미널 기반 자연스러운 채팅 환경
- **환경 데이터 통합**: 실시간 환경 정보와 함께 대화
- **건강 모니터링**: 식물 상태와 권장사항을 텍스트로 제공

## 🛠️ 기술 스택

- **AI Framework**: LangGraph, LangChain
- **LLM**: OpenAI GPT-3.5-turbo
- **MCP Integration**: langchain-mcp-adapters
- **Search Engine**: Exa Search MCP Server
- **Interface**: Terminal-based Chat
- **Data Processing**: Pandas, NumPy
- **Vector Search**: Scikit-learn, TF-IDF
- **Environment**: Python 3.8+, Node.js (MCP 서버용)

## 📊 시스템 아키텍처

```
사용자 질의
    ↓
🧠 Orchestrator (LangGraph Agent)
    ↓
질의 분석 → 필요한 도구 결정
    ↓               ↓
복합 워크플로우    단일 도구 호출
    ↓               ↓
┌─────────────────────────────────┐
│ 🔧 Tool 1: 환경 데이터 분석     │
│ 🌐 Tool 2: 웹 검색 엔진        │  
│ 📚 Tool 3: 식물 지식 RAG       │
└─────────────────────────────────┘
    ↓
정보 통합 및 분석
    ↓
🎭 식물 페르소나 응답 생성
    ↓
💬 터미널 채팅 인터페이스
```

## 🚀 설치 및 실행

### 1. 프로젝트 클론
```bash
git clone <repository-url>
cd real
```

### 2. 가상환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. 패키지 설치
```bash
pip install -r requirements.txt
```

### 4. Node.js 설치 확인 (MCP 서버용)
Exa Search MCP 서버를 실행하기 위해 Node.js가 필요합니다:
```bash
node --version
npm --version
```
Node.js가 없다면 [Node.js 공식 사이트](https://nodejs.org/)에서 설치하세요.

### 5. 환경변수 설정
`.env` 파일을 생성하고 OpenAI API 키를 추가하세요:
```bash
# .env 파일 생성
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

또는 환경변수로 직접 설정:
```bash
# Windows CMD
set OPENAI_API_KEY=your_openai_api_key_here

# Windows PowerShell 또는 Linux/Mac
export OPENAI_API_KEY=your_openai_api_key_here
```

### 6. API 데이터 처리 방식
이제 Excel 파일 대신 **API를 통해 실시간 식물 데이터**를 받아서 처리합니다:
- `temperature`: 온도 (°C)
- `humidity`: 습도 (%)  
- `light_intensity`: 광도 (lux)
- `soil_moisture`: 토양 수분 (%)

### 7. 애플리케이션 실행

#### Exa Search MCP 통합 테스트 (권장)
```bash
python test_exa_search.py
```

#### 터미널 채팅 (메인)
```bash
python chat_agent.py
```

#### 데이터 분석 테스트
```bash
python tools/data_analyzer.py
```

## 🔧 Exa Search MCP 설정

### MCP 서버 연결 확인
프로젝트는 자동으로 Exa Search MCP 서버에 연결됩니다:
- 서버 명령: `npx -y @smithery/cli@latest run exa --key [키]`
- 통신 방식: stdio
- 자동 도구 감지: web_search_exa, research_paper_search_exa 등

### 사용 가능한 Exa Search 도구들
- `web_search_exa`: 일반 웹 검색
- `research_paper_search_exa`: 학술 논문 검색  
- `wikipedia_search_exa`: Wikipedia 검색
- `company_research_exa`: 회사 정보 검색
- `crawling_exa`: URL 크롤링
- `linkedin_search_exa`: LinkedIn 검색
- `github_search_exa`: GitHub 검색

### AI 도구 선택 과정
1. 사용자가 질문 입력
2. Plant Orchestrator가 "web_search" 도구 필요성 판단
3. Exa Search MCP Agent가 질문 분석
4. 적절한 Exa Search 도구 자동 선택 및 실행
5. 결과를 Plant Persona로 변환하여 응답

## 📁 프로젝트 구조

```
real/
├── rag/                           # RAG 시스템 파일
├── tools/                         # 도구 모듈
│   ├── data_analyzer.py          # Tool 1: API 식물 데이터 분석기
│   ├── web_search_tool.py        # Tool 2: Exa Search MCP 엔진
│   └── dummy_rag_tool.py         # Tool 3: 더미 RAG 시스템
├── persona.py                   # 식물 페르소나 모듈
├── plant_orchestrator.py        # 도구 오케스트레이션 모듈
├── chat_agent.py               # 메인 채팅 에이전트 (실행)
├── api_server.py               # FastAPI 서버 (API 엔드포인트)
├── requirements.txt             # Python 패키지 의존성
├── .env.example                 # 환경변수 예시
└── README.md                    # 프로젝트 문서
```## 🌟 사용 예시

### 일반적인 대화
```
👤 사용자: "안녕! 오늘 기분이 어때?"
🌱 식물: "안녕! 오늘은 기분이 좋아! 🌟 햇살도 따뜻하게 들어오고 있어서
         잎사귀들이 반짝반짝 빛나고 있어 ✨"
```

### 환경 상태 문의 (Tool 1 - API 데이터 분석 활용)
```
👤 사용자: "지금 상태가 어때?"
🌱 식물: "지금 내 상태를 확인해볼게! 🔍
         [API 데이터 분석] 온도는 22.5°C로 딱 좋고, 습도도 45%로 적당해! 😊
         근데 토양이 좀 말라서 물이 필요할 것 같아 💧
         물 좀 줄 수 있을까? 🥺"
```

### 최신 정보 검색 (Tool 2 - Exa Search MCP 활용)
```
👤 사용자: "요즘 식물 트렌드가 뭐야?"
🌱 식물: "오! Exa Search로 찾아봤는데 🔍 
         [사용된 도구: web_search_exa]
         요즘은 공기정화 식물이 대세래! 특히 몬스테라나 스투키 같은 
         식물들이 인기가 많다고 해 🌿 나도 공기정화 능력이 있으니까 기분이 좋아! ✨"
```

### 연구 정보 검색 (Tool 2 - Research Paper Search 활용)
```
👤 사용자: "식물의 공기정화 효과에 대한 최신 연구 있어?"
🌱 식물: "좋은 질문이야! 학술 검색으로 찾아볼게 📚
         [사용된 도구: research_paper_search_exa]
         최근 NASA 연구에 따르면 실내 식물들이 포름알데히드, 벤젠 등
         유해물질을 90% 이상 제거한다고 해! 특히 스파티필름이나
         드라세나 같은 친구들이 효과가 좋다네 🌿✨"
```

### 식물 지식 문의 (Tool 3 활용)
```
👤 사용자: "라벤더 키우는 방법 알려줘"
🌱 식물: "라벤더 얘기구나! 📚 내가 알고 있는 걸 알려줄게!
         라벤더는 지중해 출신이라서 햇빛을 정말 좋아해 ☀️
         건조한 토양을 선호하고 과습에 약해서 물은 적게 주는 게 좋아!
         통풍도 잘 되어야 하고... 나랑은 좀 다른 스타일이지만
         예쁜 보라색 꽃이 향긋해서 부러워! 💜"
```

### 복합 정보 활용 (모든 도구 통합)
```
👤 사용자: "건강하게 잘 자라고 있어?"
🌱 식물: "고마워! 전반적으로 건강해! 🌿
         [API 데이터 분석] 온도: 22.5°C ✅, 습도: 45% ✅, 토양수분: 15% ⚠️
         [지식 검색] 내 종류는 적당한 물주기가 중요하다고 나와있어!
         [Exa Search - research_paper_search_exa] 최근 연구에서도 과습보다는 약간 건조한 게 좋대!
         
         종합해보니 토양이 조금 건조해서 물을 주면 완벽할 것 같아! 💚"
```

## 🎯 주요 특징

### LangGraph 워크플로우
1. **질의 분석**: 사용자 질의 내용을 분석하여 필요한 도구 조합 결정
2. **다중 도구 실행**: 필요에 따라 Tool 1, 2, 3을 단독 또는 조합 실행
3. **정보 통합**: 각 도구에서 얻은 정보를 종합하고 분석
4. **페르소나 응답**: 통합된 정보를 바탕으로 식물 페르소나 응답 생성
5. **메모리 관리**: 대화 맥락 유지 및 연속적 상호작용

### 스마트 정보 통합 시스템
- **API 데이터 분석**: 실시간 API 환경 데이터 모니터링 및 건강 상태 평가
- **Exa Search MCP**: AI가 자동으로 최적의 검색 도구를 선택하여 정보 수집
  - 일반 웹 검색, 학술 논문, Wikipedia, 회사 정보 등 다양한 소스 활용
  - MCP 프로토콜을 통한 효율적이고 안정적인 외부 도구 연동
- **지식 검색**: 전문 식물 지식 데이터베이스에서 관련 정보 추출
- **통합 분석**: 다중 소스 정보를 종합하여 정확하고 포괄적인 답변 제공

### 🔗 MCP (Model Context Protocol) 활용
- **표준화된 도구 연동**: 외부 서비스와의 안정적인 연결
- **AI 기반 도구 선택**: 질문 내용에 따라 최적의 Exa Search 도구를 자동 선택
- **확장성**: 새로운 MCP 서버 및 도구를 쉽게 추가 가능

### 생동감 있는 페르소나
- 식물의 관점에서 세상을 바라보는 독특한 시각
- 상황에 맞는 감정 표현 (기쁨, 걱정, 만족 등)
- 식물 관련 표현과 은유 사용
- 이모지를 활용한 시각적 소통

## 🔧 커스터마이징

### 모듈별 역할 분담
- **`persona.py`**: 식물 페르소나 성격, 말투, 응답 생성 담당
- **`plant_orchestrator.py`**: 질의 분석, 도구 선택, 도구 실행 담당
- **`chat_agent.py`**: 대화 관리, 터미널 인터페이스, 메인 실행 담당

### API 데이터 분석 설정
`tools/data_analyzer.py`의 `analyze_plant_health_from_api()` 메서드에서 각 환경 요소의 임계값을 조정할 수 있습니다.

### 시스템 커스터마이징
- **페르소나 수정**: `persona.py`에서 식물 성격과 말투 변경
- **도구 설정**: `plant_orchestrator.py`에서 도구 조합 로직 수정  
- **채팅 인터페이스**: `chat_agent.py`에서 터미널 인터페이스 변경

## 🤝 기여하기

1. 이 저장소를 Fork하세요
2. 새로운 기능 브랜치를 생성하세요 (`git checkout -b feature/AmazingFeature`)
3. 변경사항을 커밋하세요 (`git commit -m 'Add some AmazingFeature'`)
4. 변경사항을 푸시하세요 (`git push origin feature/AmazingFeature`)
5. Pull Request를 생성하세요

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 있습니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙋‍♀️ 문의사항

프로젝트에 대한 질문이나 제안이 있으시면 이슈를 생성해주세요.

## 🔄 최신 업데이트 (v2.0)

### ✨ Enhanced Multi-Tool System
- **GPT-3.5-turbo 전환**: 성능 최적화 및 비용 효율성 향상
- **Tool 2 추가**: 웹 검색 엔진으로 최신 정보 실시간 수집
- **Tool 3 추가**: 더미 RAG 시스템으로 전문 식물 지식 제공
- **스마트 워크플로우**: 질의에 따른 다중 도구 자동 선택 및 실행
- **정보 통합**: 환경 데이터 + 웹 정보 + 식물 지식을 종합한 포괄적 답변
- **터미널 최적화**: 간결한 터미널 기반 채팅 인터페이스로 집중

### 🎯 Tool 조합 시나리오
- **환경만**: "지금 상태 어때?" → Tool 1
- **지식만**: "장미 키우는 법?" → Tool 3  
- **최신정보만**: "요즘 식물 트렌드?" → Tool 2
- **복합질의**: "건강한가요?" → Tool 1 + 3 + 2 통합 실행

---

**🌱 터미널에서 식물 친구와 함께 즐거운 대화를 나누세요! ✨**