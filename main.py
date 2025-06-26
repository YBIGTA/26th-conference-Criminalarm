from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
from langchain_response.utils import run_langchain_from_result_file
from langchain_response.chain import diagnosis_chain
from classification import predict_disease_and_recommend
import os
import uuid
import json
import shutil

# bash에 다음을 입력해서 서버 실행
# uvicorn main:app --reload 
# request 넣을 떄 result_path 인자에 'output/result.json' 입력하면 자동으로 classification, llm 돌려서 결과 포맷메 맞게 출력됨.

app = FastAPI()

class DiagnosisRequest(BaseModel):
    input_path : str

# @app.on_event("startup")
# def startup_event():
#     try:
#         # input 불러오기
#         print("✅ classification.py 실행 완료 및 결과 파일 생성됨.")

#         # classification.py 실행
#         predict_disease_and_recommend(input_path=input_path, save_output=True, hard_coding=True) 

#         # 결과 JSON 확인
#         if not os.path.exists("output/result.json"):
#             raise FileNotFoundError("output/result.json not found")

#         print("✅ classification.py 실행 완료 및 결과 파일 생성됨.")

#     except Exception as e:
#         print(f"❌ Startup Error: {e}")


@app.post("/diagnosis")
async def diagnose(image: UploadFile = File(...)):
    try:
        # 1. 이미지 파일을 저장할 임시 경로 생성
        input_dir = "input"
        os.makedirs(input_dir, exist_ok=True)
        file_ext = os.path.splitext(image.filename)[-1]
        saved_path = os.path.join(input_dir, f"{uuid.uuid4().hex}{file_ext}")

        with open(saved_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        # 2. 분류 모델 실행
        predict_disease_and_recommend(input_path=saved_path, save_output=True, hard_coding=False)

        # 3. 결과 확인
        if not os.path.exists("output/result.json"):
            raise FileNotFoundError("output/result.json not found")

        with open("output/result.json", "r", encoding="utf-8") as f:
            result = json.load(f)

        plant = result["plant"]
        disease = result["disease"]

        # 4. LLM 처리
        return run_langchain_from_result_file(plant=plant, disease=disease)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
## 실행 결과 예시
# {
#   "plant": "스킨답서스",
#   "disease": "노균병",
#   "cause": "노균병은 주로 습도가 높은 환경에서 발생하는 곰팡이 질병입니다. 이 병은 스킨답서스의 잎에 회색이나 갈색의 반점이 생기고, 시간이 지나면 잎이 시들거나 떨어질 수 있습니다. 노균병은 특히 물빠짐이 좋지 않은 흙에서 잘 발생하며, 공기 순환이 원활하지 않은 장소에서도 쉽게 전파됩니다.",
#   "solution": "1. **환경 개선**: 스킨답서스가 자라는 장소의 습도를 낮추고, 공기 순환이 잘 되도록 해주세요. 창문을 열거나 선풍기를 사용하는 것도 도움이 됩니다.\n2. **물 주기 조절**: 과습을 피하기 위해 물 주는 빈도를 줄이고, 흙의 겉면이 마른 후에 물을 주도록 합니다.\n3. **감염된 부분 제거**: 감염된 잎이나 줄기는 즉시 잘라내어 버려주세요. 이렇게 하면 병의 확산을 막을 수 있습니다.\n4. **살균제 사용**: 필요하다면, 식물 전용 살균제를 사용하여 예방 및 치료를 할 수 있습니다. 사용 전 반드시 제품 설명서를 읽고 적절히 사용하세요. \n\n이렇게 관리하면 스킨답서스가 건강하게 자랄 수 있습니다!"
# }

