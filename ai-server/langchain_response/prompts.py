from langchain.prompts import PromptTemplate

diagnosis_prompt = PromptTemplate(
    input_variables=["plant", "disease"],
    template="""
당신은 식물 병해 진단 전문가입니다.

아래 식물과 병에 대한 정보를 기반으로, 사용자가 이해하기 쉬운 말로 설명해주세요.

식물 이름: {plant}
병 이름: {disease}

설명은 다음 형식에 맞춰 주세요:

1. 질병 설명:
2. 발생 원인:
3. 해결 방법:
"""
)
