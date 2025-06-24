# 식물 지식 더미 RAG 도구
import asyncio
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class PlantKnowledgeRAG:
    def __init__(self):
        # 더미 식물 지식 데이터베이스
        self.knowledge_base = [
            "몬스테라는 간접광을 좋아하며 물을 너무 많이 주면 뿌리가 썩을 수 있습니다.",
            "산세베리아는 건조한 환경을 선호하며 한 달에 한 번 정도 물을 주면 됩니다.",
            "스킨답서스는 초보자도 키우기 쉬운 식물로 물꽂이로도 번식이 가능합니다.",
            "고무나무는 밝은 간접광을 좋아하며 잎에 물을 뿌려주면 좋습니다.",
            "식물의 잎이 노랗게 변하는 것은 보통 과습이나 영양 부족의 신호입니다.",
            "대부분의 관엽식물은 15-25도의 온도에서 잘 자랍니다.",
            "습도가 50% 이상이면 대부분의 열대식물이 잘 자랍니다.",
            "햇빛이 너무 강하면 잎이 탈 수 있으니 커튼으로 조절해주세요.",
            "겨울철에는 물주기를 줄이고 난방기 근처는 피해주세요.",
            "분갈이는 보통 2-3년마다 한 번 정도 해주면 됩니다."
        ]
        
        # TF-IDF 벡터라이저 초기화
        self.vectorizer = TfidfVectorizer(ngram_range=(1, 2))
        self.knowledge_vectors = self.vectorizer.fit_transform(self.knowledge_base)
    
    def search_knowledge(self, query: str, top_k: int = 3):
        """지식 검색"""
        try:
            # 쿼리 벡터화
            query_vector = self.vectorizer.transform([query])
            
            # 코사인 유사도 계산
            similarities = cosine_similarity(query_vector, self.knowledge_vectors).flatten()
            
            # 상위 k개 결과 선택
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.1:  # 최소 유사도 임계값
                    results.append({
                        'content': self.knowledge_base[idx],
                        'score': float(similarities[idx])
                    })
            
            return results
            
        except Exception as e:
            print(f"지식 검색 중 오류: {e}")
            return []
    
    def get_knowledge_summary(self, query: str):
        """지식 요약 반환"""
        results = self.search_knowledge(query)
        
        if not results:
            return {
                'success': False,
                'answer': "관련 정보를 찾을 수 없어요. 다른 식물 관련 질문을 해보세요!",
                'sources': []
            }
        
        # 검색된 지식들을 조합해서 답변 생성
        knowledge_text = " ".join([r['content'] for r in results])
        
        return {
            'success': True,
            'answer': f"식물 지식베이스에서 찾은 정보예요: {knowledge_text}",
            'sources': [r['content'] for r in results]
        }


class LightRAGKnowledgeTool:
    def __init__(self):
        self.rag = PlantKnowledgeRAG()
    
    async def search_plant_knowledge(self, query: str) -> dict:
        """비동기 식물 지식 검색"""
        # 동기 함수를 비동기로 래핑
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.rag.get_knowledge_summary, query)
        return result
    
    def search_plant_knowledge_sync(self, query: str) -> dict:
        """동기 식물 지식 검색"""
        return self.rag.get_knowledge_summary(query)


# 테스트용 실행 코드
if __name__ == "__main__":
    print("🧠 더미 RAG 시스템 테스트!")
    
    rag = PlantKnowledgeRAG()
    
    # 테스트 쿼리들
    test_queries = [
        "몬스테라 키우는 방법",
        "식물 잎이 노래져요",
        "습도가 중요한가요?",
        "겨울철 관리법"
    ]
    
    for query in test_queries:
        result = rag.get_knowledge_summary(query)
        print(f"\n질문: {query}")
        print(f"답변: {result['answer'][:100]}...")
        print(f"성공: {result['success']}") 