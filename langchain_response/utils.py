import json
from .chain import diagnosis_chain

def extract_cause(text):
    return text.split("원인:")[1].split("해결")[0].strip()

def extract_solution(text):
    return text.split("해결 방법:")[1].strip()

def run_langchain_from_result_file(plant, disease):


    response = diagnosis_chain.run({
        "plant": plant,
        "disease": disease
    })

    return {
        "plant": plant,
        "disease": disease,
        "cause": extract_cause(response),
        "solution": extract_solution(response)
    }
