import os
from dotenv import load_dotenv
load_dotenv()
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from .prompts import diagnosis_prompt

# .env 에서 OPENAI_API_KEY 불러오기
load_dotenv()

llm = ChatOpenAI(
    model_name="gpt-4o-mini",  
    temperature=0.5
)

diagnosis_chain = LLMChain(
    llm=llm,
    prompt=diagnosis_prompt
)
