"""
LangGraph 기반 Plant Orchestrator 
AI-powered Tool Orchestration with Complex Workflow
"""

from typing import Dict, List, TypedDict, Annotated, Literal, Optional
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
import json

from tools.data_analyzer import EnvironmentDataAnalyzer
from tools.web_search_tool import WebSearchTool
from tools.dummy_rag_tool import PlantKnowledgeRAG

# OpenAI API 키 설정
from dotenv import load_dotenv
load_dotenv()


class OrchestratorState(TypedDict):
    """오케스트레이터 상태 정의"""
    messages: Annotated[List[BaseMessage], add_messages]
    query: str
    conversation_history: List[Dict]
    analysis_result: Dict
    tools_to_use: List[str]
    tool_results: Dict
    reasoning: str
    iteration_count: int
    is_complete: bool
    next_action: str


class PlantOrchestrator:
    """LangGraph 기반 AI 도구 오케스트레이터"""
    
    def __init__(self):
        # LLM 초기화
        self.llm = ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=0.3
        )
        
        # 도구 초기화
        self.env_analyzer = EnvironmentDataAnalyzer()
        self.web_search = WebSearchTool()
        self.rag_system = PlantKnowledgeRAG()
        
        # 도구 설명
        self.tool_descriptions = {
            "environment": "환경 데이터 분석기 - 온도, 습도, 토양수분, 광도 등 실시간 환경 상태 분석",
            "web_search": "Exa Search MCP 엔진 - AI가 검색 쿼리를 분석해서 적절한 Exa Search 도구를 선택하여 최신 정보 검색",
            "knowledge": "식물 지식 RAG - 식물 관리, 종류별 특성, 전문 지식 등 내부 데이터베이스 검색"
        }
        
        # LangGraph 워크플로우 생성
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """복잡한 LangGraph 워크플로우 생성"""
        workflow = StateGraph(OrchestratorState)
        
        # 노드 추가
        workflow.add_node("initial_analysis", self._initial_analysis_node)
        workflow.add_node("decide_tools", self._decide_tools_node)
        workflow.add_node("execute_environment", self._execute_environment_node)
        workflow.add_node("execute_web_search", self._execute_web_search_node)
        workflow.add_node("execute_knowledge", self._execute_knowledge_node)
        workflow.add_node("evaluate_completeness", self._evaluate_completeness_node)
        workflow.add_node("final_compilation", self._final_compilation_node)
        workflow.add_node("no_tools_needed", self._no_tools_needed_node)
        
        # 엣지 및 조건부 라우팅 추가
        workflow.set_entry_point("initial_analysis")
        
        # initial_analysis에서 조건부 분기
        workflow.add_conditional_edges(
            "initial_analysis",
            self._should_use_tools,
            {
                "use_tools": "decide_tools",
                "no_tools": "no_tools_needed"
            }
        )
        
        # decide_tools에서 필요한 도구별 분기
        workflow.add_conditional_edges(
            "decide_tools", 
            self._route_to_tools,
            {
                "environment": "execute_environment",
                "web_search": "execute_web_search", 
                "knowledge": "execute_knowledge",
                "evaluate": "evaluate_completeness"
            }
        )
        
        # 각 도구 실행 후 완성도 평가로
        workflow.add_edge("execute_environment", "evaluate_completeness")
        workflow.add_edge("execute_web_search", "evaluate_completeness")
        workflow.add_edge("execute_knowledge", "evaluate_completeness")
        
        # 완성도 평가에서 조건부 분기 (루프 포함)
        workflow.add_conditional_edges(
            "evaluate_completeness",
            self._check_if_complete,
            {
                "complete": "final_compilation",
                "need_more": "decide_tools",  # 다시 도구 선택으로 (루프)
                "max_iterations": "final_compilation"
            }
        )
        
        # 최종 노드들
        workflow.add_edge("final_compilation", END)
        workflow.add_edge("no_tools_needed", END)
        
        return workflow.compile()
    
    def _initial_analysis_node(self, state: OrchestratorState) -> OrchestratorState:
        """초기 질의 분석"""
        query = state["query"]
        conversation_history = state.get("conversation_history", [])
        
        # 최근 대화 내용 (최대 10개)
        recent_history = conversation_history[-10:] if conversation_history else []
        history_context = ""
        if recent_history:
            history_context = "\n\n최근 대화 내용:\n"
            for msg in recent_history:
                role = "사용자" if msg["role"] == "user" else "식물친구"
                history_context += f"{role}: {msg['content']}\n"
        
        analysis_prompt = f"""
        사용자 질문을 분석하여 도구가 필요한지 판단해주세요.

        현재 질문: "{query}"
        {history_context}

        분석해야 할 것:
        1. 이 질문이 식물 관련 정보를 필요로 하는가?
        2. 단순한 인사나 대화인가?
        3. 구체적인 데이터나 정보가 필요한가?
        4. 이전 대화 맥락을 고려했을 때 어떤 정보가 필요한가?

        응답 형식 (JSON):
        {{
            "needs_tools": true/false,
            "reasoning": "판단 이유",
            "complexity": "simple|medium|complex"
        }}
        """
        
        try:
            response = self.llm.invoke([SystemMessage(content=analysis_prompt)])
            analysis_result = json.loads(response.content)
        except:
            analysis_result = {"needs_tools": True, "reasoning": "분석 실패로 안전하게 도구 사용", "complexity": "medium"}
        
        state["analysis_result"] = analysis_result
        state["iteration_count"] = 0
        state["is_complete"] = False
        
        return state
    
    def _decide_tools_node(self, state: OrchestratorState) -> OrchestratorState:
        """AI가 어떤 도구를 사용할지 결정"""
        query = state["query"]
        current_results = state.get("tool_results", {})
        iteration = state["iteration_count"]
        
        decision_prompt = f"""
        사용자 질문을 분석하여 다음 중 어떤 도구를 사용할지 결정해주세요.

        사용자 질문: "{query}"
        현재 반복 횟수: {iteration}
        이미 수집된 정보: {list(current_results.keys())}

        사용 가능한 도구:
        1. environment: {self.tool_descriptions["environment"]}
        2. web_search: {self.tool_descriptions["web_search"]}
           - AI가 자동으로 적절한 Exa Search 도구를 선택 (web_search_exa, research_paper_search_exa, wikipedia_search_exa 등)
        3. knowledge: {self.tool_descriptions["knowledge"]}

        결정 기준:
        - 아직 수집하지 않은 정보가 있다면 해당 도구 선택
        - 이미 충분한 정보가 있다면 "evaluate"
        - 환경/상태 질문 → environment
        - 트렌드/최신 정보/연구 자료 → web_search (AI가 적절한 Exa Search 도구 자동 선택)
        - 전문 지식/관리법 → knowledge

        응답 형식 (JSON):
        {{
            "next_tool": "environment|web_search|knowledge|evaluate",
            "reasoning": "선택 이유"
        }}
        """
        
        try:
            response = self.llm.invoke([SystemMessage(content=decision_prompt)])
            decision = json.loads(response.content)
            state["next_action"] = decision.get("next_tool", "evaluate")
            state["reasoning"] = decision.get("reasoning", "")
        except:
            state["next_action"] = "evaluate"
            state["reasoning"] = "결정 실패로 평가 단계로"
        
        return state
    
    def _execute_environment_node(self, state: OrchestratorState) -> OrchestratorState:
        """환경 데이터 도구 실행 (API 버전)"""
        try:
            # API로 받은 환경 데이터를 분석
            if hasattr(self, 'current_env_data') and self.current_env_data:
                # 환경 데이터가 있는 경우 분석 수행
                env_result = self.env_analyzer.analyze_plant_health_from_api(self.current_env_data)
            else:
                # 환경 데이터가 없는 경우 기본 메시지
                env_result = "환경 데이터 분석을 위해서는 현재 센서 데이터(온도, 습도, 광도, 토양수분)가 필요합니다. API를 통해 데이터를 전달해주세요."
            
            if "tool_results" not in state:
                state["tool_results"] = {}
            state["tool_results"]["environment"] = env_result
            state["reasoning"] += " | 환경 데이터 분석 완료"
        except Exception as e:
            if "tool_results" not in state:
                state["tool_results"] = {}
            state["tool_results"]["environment_error"] = str(e)
            state["reasoning"] += f" | 환경 데이터 분석 실패: {str(e)}"
        
        state["iteration_count"] += 1
        return state
    
    def _execute_web_search_node(self, state: OrchestratorState) -> OrchestratorState:
        """Exa Search MCP 도구 실행 - AI가 적절한 검색 도구를 선택"""
        try:
            # AI Agent가 쿼리를 분석해서 적절한 Exa Search 도구를 선택하여 검색
            search_results = self.web_search.search_plant_info(state["query"])
            
            # 검색 결과 요약 생성
            web_result = {
                'query': state["query"],
                'total_results': len(search_results),
                'summary': search_results[0]['content'][:300] + "..." if search_results and search_results[0]['content'] else "검색 결과 없음",
                'sources': [r.get('source', 'Unknown') for r in search_results],
                'used_tools': search_results[0].get('used_tools', []) if search_results else [],
                'timestamp': 'Just now',
                'search_engine': 'Exa Search MCP'
            }
            
            if "tool_results" not in state:
                state["tool_results"] = {}
            state["tool_results"]["web_search"] = web_result
            
            # 사용된 Exa Search 도구들 로깅
            used_tools = web_result['used_tools']
            if used_tools:
                state["reasoning"] += f" | Exa Search 완료 (사용 도구: {', '.join(used_tools)})"
            else:
                state["reasoning"] += " | Exa Search 완료"
                
        except Exception as e:
            # 에러 발생 시 fallback 결과 제공
            error_result = {
                'query': state["query"],
                'total_results': 0,
                'summary': f"Exa Search MCP 연결 실패: {str(e)}",
                'sources': ['Fallback'],
                'used_tools': ['fallback'],
                'timestamp': 'Just now',
                'search_engine': 'Exa Search MCP (Fallback)'
            }
            
            if "tool_results" not in state:
                state["tool_results"] = {}
            state["tool_results"]["web_search"] = error_result
            state["reasoning"] += f" | Exa Search 실패 (Fallback 사용): {str(e)}"
        
        state["iteration_count"] += 1
        return state
    
    def _execute_knowledge_node(self, state: OrchestratorState) -> OrchestratorState:
        """지식 검색 도구 실행"""
        try:
            knowledge_result = self.rag_system.get_knowledge_summary(state["query"])
            if "tool_results" not in state:
                state["tool_results"] = {}
            state["tool_results"]["knowledge"] = knowledge_result
            state["reasoning"] += " | 지식 검색 완료"
        except Exception as e:
            state["tool_results"]["knowledge_error"] = str(e)
        
        state["iteration_count"] += 1
        return state
    
    def _evaluate_completeness_node(self, state: OrchestratorState) -> OrchestratorState:
        """AI가 수집된 정보가 충분한지 평가"""
        query = state["query"]
        current_results = state.get("tool_results", {})
        iteration = state["iteration_count"]
        
        evaluation_prompt = f"""
        사용자 질문에 답하기 위해 수집된 정보가 충분한지 평가해주세요.

        사용자 질문: "{query}"
        수집된 정보: {list(current_results.keys())}
        현재 반복 횟수: {iteration}

        평가 기준:
        1. 질문에 답하기 위한 핵심 정보가 모두 있는가?
        2. 추가로 필요한 정보가 있는가?
        3. 이미 3번 이상 반복했다면 충분하다고 판단

        응답 형식 (JSON):
        {{
            "is_complete": true/false,
            "missing_info": "부족한 정보 설명",
            "confidence": 0.8
        }}
        """
        
        try:
            response = self.llm.invoke([SystemMessage(content=evaluation_prompt)])
            evaluation = json.loads(response.content)
            state["is_complete"] = evaluation.get("is_complete", True)
            state["reasoning"] += f" | 완성도 평가: {evaluation.get('confidence', 0.5)}"
        except:
            state["is_complete"] = True  # 평가 실패 시 완료로 처리
        
        return state
    
    def _final_compilation_node(self, state: OrchestratorState) -> OrchestratorState:
        """최종 결과 컴파일"""
        state["is_complete"] = True
        state["reasoning"] += " | 최종 컴파일 완료"
        return state
    
    def _no_tools_needed_node(self, state: OrchestratorState) -> OrchestratorState:
        """도구 없이 처리 가능한 경우"""
        state["is_complete"] = True
        state["tool_results"] = {}
        state["reasoning"] = "도구 없이 일반 대화로 처리"
        return state
    
    # 조건부 라우팅 함수들
    def _should_use_tools(self, state: OrchestratorState) -> Literal["use_tools", "no_tools"]:
        """도구 사용 여부 결정"""
        analysis = state.get("analysis_result", {})
        return "use_tools" if analysis.get("needs_tools", True) else "no_tools"
    
    def _route_to_tools(self, state: OrchestratorState) -> Literal["environment", "web_search", "knowledge", "evaluate"]:
        """다음 도구 라우팅"""
        return state.get("next_action", "evaluate")
    
    def _check_if_complete(self, state: OrchestratorState) -> Literal["complete", "need_more", "max_iterations"]:
        """완성도 체크"""
        if state["iteration_count"] >= 3:  # 최대 3번 반복
            return "max_iterations"
        elif state.get("is_complete", False):
            return "complete"
        else:
            return "need_more"
    
    def analyze_and_execute(self, query: str, conversation_history: List[Dict] = None, env_data: Optional[Dict] = None) -> Dict:
        """메인 인터페이스: 복잡한 LangGraph 워크플로우 실행"""
        try:
            # 환경 데이터 설정 (API에서 받은 데이터)
            if env_data:
                self.current_env_data = env_data
            
            # 초기 상태 생성
            initial_state = OrchestratorState(
                messages=[HumanMessage(content=query)],
                query=query,
                conversation_history=conversation_history or [],
                analysis_result={},
                tools_to_use=[],
                tool_results={},
                reasoning="",
                iteration_count=0,
                is_complete=False,
                next_action=""
            )
            
            # 복잡한 워크플로우 실행
            result = self.workflow.invoke(initial_state)
            
            # 결과 정리
            tools_used = list(result.get("tool_results", {}).keys())
            
            return {
                "query_analysis": {
                    "query_type": result["analysis_result"].get("complexity", "unknown"),
                    "tools_needed": tools_used,
                    "reasoning": result["reasoning"],
                    "confidence": 0.9,
                    "iterations": result["iteration_count"]
                },
                "tool_results": result.get("tool_results", {}),
                "reasoning": result["reasoning"],
                "workflow_path": f"반복 {result['iteration_count']}회, 사용 도구: {tools_used}",
                "success": True
            }
            
        except Exception as e:
            return {
                "query_analysis": {"query_type": "error", "tools_needed": [], "reasoning": f"오류: {str(e)}", "confidence": 0.0},
                "tool_results": {"error": str(e)},
                "reasoning": f"워크플로우 실행 중 오류: {str(e)}",
                "workflow_path": "오류로 인한 중단",
                "success": False
            }
    
    def get_available_tools(self) -> Dict:
        """사용 가능한 도구 목록 및 설명 반환"""
        return self.tool_descriptions


# 테스트용 실행 코드
if __name__ == "__main__":
    orchestrator = PlantOrchestrator()
    
    print("=== 복잡한 LangGraph 워크플로우 테스트 ===")
    
    # 테스트 질의들
    test_queries = [
        "내 상태 어때?",
        "요즘 식물 트렌드는?", 
        "몬스테라 키우는 법?",
        "건강하게 잘 자라고 있어? 요즘 유행하는 관리법도 알려줘",
        "안녕!"
    ]
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"🔍 질의: {query}")
        
        result = orchestrator.analyze_and_execute(query)
        
        print(f"🧠 AI 분석: {result['query_analysis']['query_type']}")
        print(f"🔧 사용된 도구: {result['query_analysis']['tools_needed']}")
        print(f"🛤️ 워크플로우 경로: {result['workflow_path']}")
        print(f"💭 AI 추론: {result['reasoning']}")
        print(f"📊 신뢰도: {result['query_analysis'].get('confidence', 'N/A')}")
        
        if result['tool_results']:
            print(f"📦 도구 실행 결과: {list(result['tool_results'].keys())}")
            
        print(f"✅ 성공: {result['success']}")