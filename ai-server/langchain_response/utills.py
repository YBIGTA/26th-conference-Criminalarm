import json
from .chain import diagnosis_chain

def run_langchain_from_result_file(result_path="output/result.json"):
    with open(result_path, "r", encoding="utf-8") as f:
        result = json.load(f)

    plant = result["plant"]
    disease = result["disease"]

    response = diagnosis_chain.run({
        "plant": plant,
        "disease": disease
    })

    return {
        "plant": plant,
        "disease": disease,
        "response": response
    }
