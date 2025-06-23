import json
import os
from pathlib import Path
from langchain_response.utills import run_langchain_from_result_file
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
    print(f"[INFO] 결과 파일 경로: {result_path}")
    
    # 2) 파일이 잘 있는지 확인
    if not result_path.exists():
        print(f"[ERROR] {result_path} 파일을 찾을 수 없습니다.")
        return

    try:
        # 파일 읽기
        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print("[INFO] 파일을 성공적으로 읽었습니다.")
            print(f"[INFO] 파일 내용: {json.dumps(data, ensure_ascii=False, indent=2)}")
    except json.JSONDecodeError as e:
        print(f"[ERROR] JSON 파일 파싱 중 오류 발생: {str(e)}")
        return
    except Exception as e:
        print(f"[ERROR] 파일 읽기 중 오류 발생: {str(e)}")
        return

    # 3) LangChain 실행
    try:
        print("[INFO] LangChain 실행 시작")
        output = run_langchain_from_result_file(str(result_path))
        if isinstance(output, dict) and "error" in output:
            print(f"[ERROR] LLM 실행 중 오류 발생: {output['error']}")
        else:
            # 4) 결과 예쁘게 출력
            print("\n=== LLM 응답 결과 ===")
            print(json.dumps(output, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"[ERROR] LLM 실행 중 오류 발생: {str(e)}")
        import traceback
        print(f"[ERROR] 상세 에러: {traceback.format_exc()}")

if __name__ == "__main__":
    print("=== 테스트 시작 ===")
    main()
    print("=== 테스트 종료 ===")
