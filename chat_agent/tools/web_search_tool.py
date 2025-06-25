"""
Tool 2: 웹 검색 엔진 (네이버 API 사용)
Web Search Engine for Latest Plant Information using Naver API
"""

import requests
import json
from typing import List, Dict, Optional
import urllib.parse
import os
import logging

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class WebSearchTool:
    """네이버 검색 API를 사용한 식물 관련 최신 정보 검색 도구"""
    
    def __init__(self):
        # 네이버 API 키 설정
        self.client_id = "cIchWx3damfG74qMyJgv"
        self.client_secret = "jE1ZgoxNLg"
        
        self.headers = {
            'X-Naver-Client-Id': self.client_id,
            'X-Naver-Client-Secret': self.client_secret,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # 네이버 검색 API 엔드포인트
        self.search_url = "https://openapi.naver.com/v1/search/blog.json"
        
        logger.info("🔍 WebSearchTool 초기화 완료")
        logger.info(f"📡 네이버 API 엔드포인트: {self.search_url}")
        
    def search_plant_info(self, query: str, max_results: int = 3) -> List[Dict]:
        """네이버 블로그 검색을 통한 식물 정보 검색"""
        logger.info(f"🔍 검색 시작: '{query}' (최대 {max_results}개 결과)")
        
        try:
            # 식물 관련 검색어로 보강
            enhanced_query = f"식물 {query} 키우기 관리"
            logger.info(f"🔧 보강된 검색어: '{enhanced_query}'")
            
            # 네이버 검색 API 호출
            params = {
                'query': enhanced_query,
                'display': max_results,
                'start': 1,
                'sort': 'sim'  # 정확도순 정렬
            }
            
            logger.info(f"📤 네이버 API 요청 시작...")
            logger.info(f"   - URL: {self.search_url}")
            logger.info(f"   - 파라미터: {params}")
            logger.info(f"   - 헤더: X-Naver-Client-Id: {self.client_id[:10]}...")
            
            response = requests.get(
                self.search_url,
                headers=self.headers,
                params=params,
                timeout=10
            )
            
            logger.info(f"📥 네이버 API 응답 받음: HTTP {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                total_results = data.get('total', 0)
                items = data.get('items', [])
                
                logger.info(f"✅ 검색 성공!")
                logger.info(f"   - 전체 결과 수: {total_results}")
                logger.info(f"   - 반환된 항목 수: {len(items)}")
                
                # 각 결과 미리보기
                for i, item in enumerate(items[:3]):
                    title = self._clean_html_tags(item.get('title', ''))[:50]
                    logger.info(f"   - 결과 #{i+1}: {title}...")
                
                processed_results = self._process_naver_results(items)
                logger.info(f"🎯 최종 처리된 결과: {len(processed_results)}개")
                return processed_results
                
            else:
                logger.error(f"❌ 네이버 API 오류: HTTP {response.status_code}")
                logger.error(f"   - 응답 내용: {response.text[:200]}...")
                logger.info("🔄 Fallback 데이터 사용")
                return self._get_fallback_results(query)
                
        except Exception as e:
            logger.error(f"💥 검색 중 예외 발생: {str(e)}")
            logger.info("🔄 Fallback 데이터 사용")
            return self._get_fallback_results(query)
    
    def _process_naver_results(self, items: List[Dict]) -> List[Dict]:
        """네이버 검색 결과 처리"""
        logger.info(f"🔧 검색 결과 처리 시작: {len(items)}개 항목")
        
        results = []
        
        for i, item in enumerate(items):
            # HTML 태그 제거
            title = self._clean_html_tags(item.get('title', ''))
            description = self._clean_html_tags(item.get('description', ''))
            
            result = {
                'title': title,
                'content': description,
                'source': item.get('bloggername', '네이버 블로그'),
                'url': item.get('link', ''),
                'date': item.get('postdate', ''),
                'relevance_score': 0.9 - (i * 0.1)
            }
            
            results.append(result)
            
            logger.info(f"   - 처리 완료 #{i+1}:")
            logger.info(f"     제목: {title[:50]}...")
            logger.info(f"     내용: {description[:80]}...")
            logger.info(f"     출처: {result['source']}")
            
        logger.info(f"✅ 결과 처리 완료: {len(results)}개")
        return results
    
    def _clean_html_tags(self, text: str) -> str:
        """HTML 태그 제거 및 텍스트 정리"""
        import re
        
        # HTML 태그 제거
        text = re.sub(r'<[^>]+>', '', text)
        # HTML 엔티티 변환
        text = text.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        text = text.replace('&quot;', '"').replace('&#39;', "'")
        
        return text.strip()
    
    def _get_fallback_results(self, query: str) -> List[Dict]:
        """API 호출 실패 시 대체 결과"""
        logger.info(f"🛡️ Fallback 데이터 생성 중: '{query}'")
        
        fallback_info = {
            '몬스테라': '몬스테라는 밝은 간접광을 좋아하고, 토양이 마르면 충분히 물을 주세요. 습도가 높은 환경을 선호해요.',
            '고무나무': '고무나무는 키우기 쉬운 식물로, 밝은 곳에서 기르고 겉흙이 말랐을 때 물을 주면 됩니다.',
            '산세베리아': '산세베리아는 물을 적게 줘도 되는 식물이에요. 한 달에 1-2번 정도면 충분해요.',
            '스투키': '스투키는 공기정화 효과가 뛰어나고, 물을 자주 주지 않아도 잘 자라는 식물이에요.'
        }
        
        # 쿼리에서 식물 이름 찾기
        plant_info = "식물은 적절한 물주기와 빛이 중요해요. 각 식물의 특성에 맞게 관리해주세요!"
        matched_plant = "일반"
        
        for plant_name, info in fallback_info.items():
            if plant_name in query:
                plant_info = info
                matched_plant = plant_name
                break
        
        logger.info(f"   - 매칭된 식물: {matched_plant}")
        logger.info(f"   - 제공할 정보: {plant_info[:50]}...")
        
        result = [{
            'title': f'{query} 관련 정보',
            'content': plant_info,
            'source': '식물 관리 가이드',
            'url': 'https://plant-care-guide.com',
            'relevance_score': 0.7
        }]
        
        logger.info(f"🛡️ Fallback 결과 생성 완료: 1개")
        return result
    
    def search_trends(self, topic: str = "식물 트렌드") -> str:
        """최신 식물 트렌드 검색"""
        logger.info(f"📈 트렌드 검색: '{topic}'")
        
        results = self.search_plant_info(f"2024 최신 {topic}")
        
        if results:
            trend_info = []
            for result in results:
                trend_info.append(f"• {result['content'][:100]}...")
            
            final_result = f"🔍 **최신 {topic} 정보**:\n" + "\n".join(trend_info)
            logger.info(f"📈 트렌드 검색 완료: {len(results)}개 결과")
            return final_result
        else:
            logger.warning(f"📈 트렌드 검색 실패: '{topic}'")
            return f"죄송해요, {topic} 정보를 찾지 못했어요 😅"
    
    def search_care_tips(self, plant_name: str) -> str:
        """특정 식물 관리 팁 검색"""
        logger.info(f"🌿 관리 팁 검색: '{plant_name}'")
        
        results = self.search_plant_info(f"{plant_name} 관리 키우기")
        
        if results:
            tips = []
            for result in results:
                tips.append(f"📌 {result['content'][:150]}...")
            
            final_result = f"🌿 **{plant_name} 관리 팁**:\n" + "\n".join(tips)
            logger.info(f"🌿 관리 팁 검색 완료: {len(results)}개 결과")
            return final_result
        else:
            logger.warning(f"🌿 관리 팁 검색 실패: '{plant_name}'")
            return f"{plant_name}에 대한 정보를 찾지 못했어요. 일반적인 식물 관리 방법을 알려드릴까요? 🤔"
    
    def search_plant_problems(self, problem: str) -> str:
        """식물 문제 해결 정보 검색"""
        logger.info(f"🚨 문제 해결 검색: '{problem}'")
        
        results = self.search_plant_info(f"식물 {problem} 해결 방법")
        
        if results:
            solutions = []
            for result in results:
                solutions.append(f"💡 {result['content'][:120]}...")
            
            final_result = f"🚨 **{problem} 해결 방법**:\n" + "\n".join(solutions)
            logger.info(f"🚨 문제 해결 검색 완료: {len(results)}개 결과")
            return final_result
        else:
            logger.warning(f"🚨 문제 해결 검색 실패: '{problem}'")
            return f"{problem}에 대한 해결책을 찾지 못했어요. 전문가에게 문의해보시는 것을 추천해요! 🌱"
    
    def get_web_summary(self, query: str) -> Dict:
        """웹 검색 결과 요약"""
        logger.info(f"📊 검색 요약 생성: '{query}'")
        
        results = self.search_plant_info(query)
        
        if not results:
            logger.warning(f"📊 검색 요약 실패: 결과 없음")
            return {
                'summary': '검색 결과가 없어요 😔',
                'sources': 0,
                'confidence': 0.0
            }
        
        # 결과 요약
        all_content = []
        sources = []
        
        for result in results:
            all_content.append(result['content'][:200])  # 길이 제한
            sources.append(result['source'])
        
        summary = " ".join(all_content)
        confidence = sum(r.get('relevance_score', 0.5) for r in results) / len(results)
        
        summary_result = {
            'summary': summary,
            'sources': len(sources),
            'confidence': confidence,
            'source_list': sources
        }
        
        logger.info(f"📊 검색 요약 완료:")
        logger.info(f"   - 요약 길이: {len(summary)} 문자")
        logger.info(f"   - 출처 수: {len(sources)}")
        logger.info(f"   - 신뢰도: {confidence:.2f}")
        
        return summary_result


# 테스트용 실행 코드
if __name__ == "__main__":
    print("=== 네이버 API 웹 검색 도구 디버깅 테스트 ===")
    
    search_tool = WebSearchTool()
    
    # 트렌드 검색 테스트
    print("\n" + "="*50)
    print("1. 트렌드 검색 테스트")
    print("="*50)
    trend_result = search_tool.search_trends("실내식물 트렌드")
    print(f"결과:\n{trend_result}")
    
    # 관리 팁 검색 테스트
    print("\n" + "="*50)
    print("2. 관리 팁 검색 테스트")
    print("="*50)
    care_result = search_tool.search_care_tips("몬스테라")
    print(f"결과:\n{care_result}")
    
    # 문제 해결 검색 테스트
    print("\n" + "="*50)
    print("3. 문제 해결 검색 테스트")
    print("="*50)
    problem_result = search_tool.search_plant_problems("잎이 노래짐")
    print(f"결과:\n{problem_result}")
    
    # 일반 검색 테스트
    print("\n" + "="*50)
    print("4. 일반 검색 테스트")
    print("="*50)
    general_result = search_tool.get_web_summary("식물 물주기")
    print(f"요약: {general_result['summary'][:200]}...")
    print(f"신뢰도: {general_result['confidence']:.2f}")
    print(f"출처: {general_result['source_list']}")