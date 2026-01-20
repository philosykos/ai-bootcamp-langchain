"""
환경 변수 및 LLM 설정
"""
from dotenv import load_dotenv
import os
from langchain_openai import AzureChatOpenAI

# 환경 변수 로드
load_dotenv()

# Azure OpenAI 설정
AOAI_ENDPOINT = os.getenv("AOAI_ENDPOINT")
AOAI_API_KEY = os.getenv("AOAI_API_KEY")
AOAI_DEPLOY_GPT4O = os.getenv("AOAI_DEPLOY_GPT4O")
AOAI_DEPLOY_GPT4O_MINI = os.getenv("AOAI_DEPLOY_GPT4O_MINI")
AOAI_DEPLOY_EMBED_3_LARGE = os.getenv("AOAI_DEPLOY_EMBED_3_LARGE")
AOAI_DEPLOY_EMBED_3_SMALL = os.getenv("AOAI_DEPLOY_EMBED_3_SMALL")
AOAI_DEPLOY_EMBED_ADA = os.getenv("AOAI_DEPLOY_EMBED_ADA")

def get_llm(temperature: float = 0) -> AzureChatOpenAI:
    """Azure OpenAI LLM 인스턴스를 반환합니다.
    
    Args:
        temperature: 생성 온도 (0.0 ~ 2.0)
        
    Returns:
        AzureChatOpenAI 인스턴스
    """
    return AzureChatOpenAI(
        azure_endpoint=AOAI_ENDPOINT,
        azure_deployment=AOAI_DEPLOY_GPT4O,
        api_version="2024-10-21",
        api_key=AOAI_API_KEY,
        temperature=temperature
    )