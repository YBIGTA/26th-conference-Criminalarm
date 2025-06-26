"""
Tool 1: 환경 데이터 분석기 (API 버전)
Environment Data Analyzer for Plant Health Monitoring - API Version
"""

from typing import Dict, List, Optional, Tuple, Union
import logging

logger = logging.getLogger(__name__)


class EnvironmentDataAnalyzer:
    """API로 전달받은 환경 데이터를 분석하여 식물 건강 상태를 평가하는 도구"""
    
    def __init__(self):
        """API 버전 - data 폴더 의존성 제거"""
        self.thresholds = {
            'temperature': {'min': 18, 'max': 28, 'optimal_min': 20, 'optimal_max': 25},
            'humidity': {'min': 30, 'max': 70, 'optimal_min': 40, 'optimal_max': 60},
            'light_intensity': {'min': 200, 'max': 2000, 'optimal_min': 500, 'optimal_max': 1500},
            'soil_moisture': {'min': 20, 'max': 80, 'optimal_min': 40, 'optimal_max': 70}
        }
        logger.info("🔬 EnvironmentDataAnalyzer (API 버전) 초기화 완료")
    
    def analyze_plant_health_from_api(self, plant_data: Dict[str, Optional[float]]) -> Dict:
        """API로 전달받은 식물 데이터를 분석"""
        logger.info(f"🌱 API 식물 데이터 분석 시작: {plant_data}")
        
        # 유효한 데이터만 필터링
        valid_readings = {}
        for key, value in plant_data.items():
            if value is not None and key in self.thresholds:
                valid_readings[key] = float(value)
        
        logger.info(f"📊 유효한 데이터: {valid_readings}")
        
        analysis = {
            'current_readings': valid_readings,
            'health_score': 0,
            'status_details': {},
            'recommendations': [],
            'overall_status': 'unknown',
            'alerts': []
        }
        
        if not valid_readings:
            logger.warning("⚠️ 유효한 식물 데이터가 없음")
            analysis['overall_status'] = 'no_data'
            analysis['recommendations'].append("식물 센서 데이터를 확인해주세요.")
            return analysis
        
        total_score = 0
        max_score = 0
        
        for sensor_type, value in valid_readings.items():
            if sensor_type in self.thresholds:
                threshold = self.thresholds[sensor_type]
                status, score, recommendation = self._evaluate_sensor(sensor_type, value, threshold)
                
                analysis['status_details'][sensor_type] = {
                    'value': value,
                    'status': status,
                    'score': score,
                    'recommendation': recommendation
                }
                
                total_score += score
                max_score += 100
                
                if score < 70:  # 경고 임계값
                    analysis['alerts'].append(f"{sensor_type}: {recommendation}")
        
        # 전체 건강 점수 계산
        if max_score > 0:
            analysis['health_score'] = round((total_score / max_score) * 100, 1)
        
        # 전체 상태 결정
        if analysis['health_score'] >= 80:
            analysis['overall_status'] = 'excellent'
        elif analysis['health_score'] >= 60:
            analysis['overall_status'] = 'good'
        elif analysis['health_score'] >= 40:
            analysis['overall_status'] = 'fair'
        else:
            analysis['overall_status'] = 'poor'
        
        logger.info(f"✅ 분석 완료 - 건강도: {analysis['health_score']}점, 상태: {analysis['overall_status']}")
        return analysis
    
    def _evaluate_sensor(self, sensor_type: str, value: float, threshold: Dict) -> Tuple[str, int, str]:
        """개별 센서 수치 평가"""
        if threshold['optimal_min'] <= value <= threshold['optimal_max']:
            return 'optimal', 100, f"{sensor_type.title()} 수치가 완벽해요! ✅"
        elif threshold['min'] <= value <= threshold['max']:
            if value < threshold['optimal_min']:
                return 'low_normal', 80, f"{sensor_type.title()}가 조금 낮아요. 조금만 더 신경써주세요 🔄"
            else:
                return 'high_normal', 80, f"{sensor_type.title()}가 조금 높아요. 조금만 더 주의해주세요 🔄"
        elif value < threshold['min']:
            return 'critical_low', 30, f"{sensor_type.title()}가 너무 낮아요! 즉시 조치가 필요해요 🚨"
        else:
            return 'critical_high', 30, f"{sensor_type.title()}가 너무 높아요! 즉시 조치가 필요해요 🚨"
    
    def get_environmental_summary_from_api(self, plant_data: Dict[str, Optional[float]]) -> str:
        """API 데이터로부터 환경 상태 요약 텍스트 반환"""
        analysis = self.analyze_plant_health_from_api(plant_data)
        
        readings = analysis['current_readings']
        health_score = analysis['health_score']
        overall_status = analysis['overall_status']
        
        # 상태별 이모지
        status_emojis = {
            'excellent': '🌟',
            'good': '😊', 
            'fair': '😐',
            'poor': '😰',
            'no_data': '🤔'
        }
        
        emoji = status_emojis.get(overall_status, '🤔')
        
        if overall_status == 'no_data':
            return "식물 센서 데이터가 없어서 상태를 확인할 수 없어요. 센서를 확인해주세요! 🤔"
        
        summary = f"""현재 내 환경 상태를 확인해봤어! {emoji}

🌡️ **온도**: {readings.get('temperature', '데이터 없음')}°C
💧 **습도**: {readings.get('humidity', '데이터 없음')}%  
☀️ **광도**: {readings.get('light_intensity', '데이터 없음')} lux
🌱 **토양수분**: {readings.get('soil_moisture', '데이터 없음')}%

**전체 건강도**: {health_score}점 ({overall_status})

"""
        
        # 경고사항 추가
        if analysis['alerts']:
            summary += "⚠️ **주의사항**:\n"
            for alert in analysis['alerts']:
                summary += f"- {alert}\n"
        
        return summary
    
    def get_status_for_api_response(self, sensor_type: str, value: Optional[float]) -> str:
        """API 응답용 간단한 상태 반환"""
        if value is None or sensor_type not in self.thresholds:
            return "정보 없음"
        
        threshold = self.thresholds[sensor_type]
        status, _, _ = self._evaluate_sensor(sensor_type, value, threshold)
        
        status_mapping = {
            'optimal': '좋음',
            'low_normal': '보통',
            'high_normal': '보통',
            'critical_low': '나쁨',
            'critical_high': '나쁨'
        }
        
        return status_mapping.get(status, '알 수 없음')
    
    def get_recommendations_from_api(self, plant_data: Dict[str, Optional[float]]) -> List[str]:
        """API 데이터로부터 추천사항 반환"""
        analysis = self.analyze_plant_health_from_api(plant_data)
        recommendations = []
        
        for sensor_type, details in analysis['status_details'].items():
            if details['score'] < 80:  # 개선이 필요한 경우
                recommendations.append(details['recommendation'])
        
        if not recommendations:
            recommendations.append("현재 식물 상태가 좋습니다! 계속 잘 관리해주세요! 🌱")
        
        return recommendations[:3]  # 최대 3개까지
    
    # 하위 호환성을 위한 기존 메서드들 (deprecated)
    def get_current_readings(self) -> Dict[str, float]:
        """하위 호환성용 - 사용하지 않음"""
        logger.warning("⚠️ get_current_readings는 더 이상 사용되지 않습니다. API 데이터를 직접 전달하세요.")
        return {
            'temperature': 22.5,
            'humidity': 45.0,
            'light_intensity': 800.0,
            'soil_moisture': 35.0
        }
    
    def analyze_plant_health(self) -> Dict:
        """하위 호환성용 - 사용하지 않음"""
        logger.warning("⚠️ analyze_plant_health는 더 이상 사용되지 않습니다. analyze_plant_health_from_api를 사용하세요.")
        default_data: Dict[str, Optional[float]] = {
            'temperature': 22.5,
            'humidity': 45.0,
            'light_intensity': 800.0,
            'soil_moisture': 35.0
        }
        return self.analyze_plant_health_from_api(default_data)


# 테스트용 실행 코드
if __name__ == "__main__":
    analyzer = EnvironmentDataAnalyzer()
    
    print("=== 환경 데이터 분석기 (API 버전) 테스트 ===")
    
    # 테스트 데이터
    test_data: Dict[str, Optional[float]] = {
        'temperature': 25.0,
        'humidity': 55.0,
        'light_intensity': 800.0,
        'soil_moisture': 45.0
    }
    
    # 건강 상태 분석
    health = analyzer.analyze_plant_health_from_api(test_data)
    print(f"건강 점수: {health['health_score']}")
    print(f"전체 상태: {health['overall_status']}")
    
    # 요약 텍스트
    summary = analyzer.get_environmental_summary_from_api(test_data)
    print("\n=== 환경 상태 요약 ===")
    print(summary)
    
    # 개별 상태 확인
    print("\n=== 개별 센서 상태 ===")
    for sensor_type, value in test_data.items():
        status = analyzer.get_status_for_api_response(sensor_type, value)
        print(f"{sensor_type}: {value} -> {status}")
    
    # 추천사항
    recommendations = analyzer.get_recommendations_from_api(test_data)
    print(f"\n=== 추천사항 ===")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")