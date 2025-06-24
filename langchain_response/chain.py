import os
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from .prompts import diagnosis_prompt


llm = ChatOpenAI(
    model_name="gpt-4o-mini",
    openai_api_key="your_key",  
    temperature=0.5
)

diagnosis_chain = LLMChain(
    llm=llm,
    prompt=diagnosis_prompt
)
