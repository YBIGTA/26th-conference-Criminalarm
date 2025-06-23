from langchain_response.chain import diagnosis_chain

response = diagnosis_chain.run({
    "plant": "스킨답서스",
    "disease": "노균병"
})

print(response)
