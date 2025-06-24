import json
import os
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def main():
    print("[INFO] 스크립트 시작")
    print(f"[INFO] 현재 디렉토리: {os.getcwd()}")
    
    # 1) result.json 경로 지정
    # 현재 디렉토리 기준으로 상대 경로 사용
    current_dir = Path(__file__).parent
    result_path = current_dir.parent / "output" / "result.json"