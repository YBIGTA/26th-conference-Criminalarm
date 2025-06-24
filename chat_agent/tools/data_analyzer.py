"""
Tool 1: 환경 데이터 분석기
Environment Data Analyzer for Plant Health Monitoring
"""

import pandas as pd
import numpy as np
import os
import glob
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
warnings.filterwarnings('ignore')


class EnvironmentDataAnalyzer:
    """환경 데이터를 분석하여 식물 건강 상태를 평가하는 도구"""
    
    def __init__(self, data_path: str = "data/"):
        self.data_path = data_path
        self.thresholds = {
            'temperature': {'min': 18, 'max': 28, 'optimal_min': 20, 'optimal_max': 25},
            'humidity': {'min': 30, 'max': 70, 'optimal_min': 40, 'optimal_max': 60},
            'light_intensity': {'min': 200, 'max': 2000, 'optimal_min': 500, 'optimal_max': 1500},
            'soil_moisture': {'min': 20, 'max': 80, 'optimal_min': 40, 'optimal_max': 70}
        }    
    def load_data(self) -> Dict[str, pd.DataFrame]:
        """모든 환경 데이터 파일을 로드"""
        data = {}
        
        file_mappings = {
            'temperature': 'Environment Temperature.xlsx',
            'humidity': 'Environment Humidity.xlsx', 
            'light_intensity': 'Environment Light Intensity.xlsx',
            'soil_moisture': 'Soil Moisture.xlsx'
        }
        
        for key, filename in file_mappings.items():
            file_path = os.path.join(self.data_path, filename)
            try:
                if os.path.exists(file_path):
                    df = pd.read_excel(file_path)
                    # 첫 번째 컬럼을 datetime으로 변환 시도
                    if len(df.columns) >= 2:
                        try:
                            df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
                            df.columns = ['timestamp', 'value']
                        except:
                            # datetime 변환 실패 시 기본 컬럼명 사용
                            df.columns = ['timestamp', 'value']
                    data[key] = df
                else:
                    print(f"Warning: {filename} not found")
            except Exception as e:
                print(f"Error loading {filename}: {str(e)}")
        
        return data    
    def get_current_readings(self) -> Dict[str, float]:
        """현재 환경 수치 반환 (최신 데이터 또는 시뮬레이션)"""
        data = self.load_data()
        current_readings = {}
        
        for sensor_type, df in data.items():
            if not df.empty and 'value' in df.columns:
                # 최신 데이터 가져오기
                latest_value = df['value'].iloc[-1]
                current_readings[sensor_type] = float(latest_value)
            else:
                # 데이터가 없으면 시뮬레이션 값 생성
                current_readings[sensor_type] = self._generate_simulated_value(sensor_type)
        
        # 기본값 설정 (데이터가 전혀 없는 경우)
        defaults = {
            'temperature': 22.5,
            'humidity': 45.0,
            'light_intensity': 800.0,
            'soil_moisture': 35.0
        }
        
        for key, default_val in defaults.items():
            if key not in current_readings:
                current_readings[key] = default_val
                
        return current_readings
    
    def _generate_simulated_value(self, sensor_type: str) -> float:
        """시뮬레이션 값 생성"""
        ranges = {
            'temperature': (18, 28),
            'humidity': (30, 70),
            'light_intensity': (200, 2000),
            'soil_moisture': (20, 80)
        }
        
        if sensor_type in ranges:
            min_val, max_val = ranges[sensor_type]
            return round(np.random.uniform(min_val, max_val), 1)
        return 0.0    
    def analyze_plant_health(self) -> Dict:
        """식물 건강 상태 종합 분석"""
        readings = self.get_current_readings()
        analysis = {
            'current_readings': readings,
            'health_score': 0,
            'status_details': {},
            'recommendations': [],
            'overall_status': 'unknown',
            'alerts': []
        }
        
        total_score = 0
        max_score = 0
        
        for sensor_type, value in readings.items():
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
    
    def get_environmental_summary(self) -> str:
        """환경 상태 요약 텍스트 반환"""
        analysis = self.analyze_plant_health()
        
        readings = analysis['current_readings']
        health_score = analysis['health_score']
        overall_status = analysis['overall_status']
        
        # 상태별 이모지
        status_emojis = {
            'excellent': '🌟',
            'good': '😊', 
            'fair': '😐',
            'poor': '😰'
        }
        
        emoji = status_emojis.get(overall_status, '🤔')
        
        summary = f"""현재 내 환경 상태를 확인해봤어! {emoji}

🌡️ **온도**: {readings.get('temperature', 0):.1f}°C
💧 **습도**: {readings.get('humidity', 0):.1f}%  
☀️ **광도**: {readings.get('light_intensity', 0):.0f} lux
🌱 **토양수분**: {readings.get('soil_moisture', 0):.1f}%

**전체 건강도**: {health_score}점 ({overall_status})

"""
        
        # 경고사항 추가
        if analysis['alerts']:
            summary += "⚠️ **주의사항**:\n"
            for alert in analysis['alerts']:
                summary += f"- {alert}\n"
        
        return summary


# 테스트용 실행 코드
if __name__ == "__main__":
    analyzer = EnvironmentDataAnalyzer()
    
    print("=== 환경 데이터 분석기 테스트 ===")
    
    # 현재 수치 확인
    readings = analyzer.get_current_readings()
    print(f"현재 수치: {readings}")
    
    # 건강 상태 분석
    health = analyzer.analyze_plant_health()
    print(f"건강 점수: {health['health_score']}")
    print(f"전체 상태: {health['overall_status']}")
    
    # 요약 텍스트
    summary = analyzer.get_environmental_summary()
    print("\n=== 환경 상태 요약 ===")
    print(summary)