"""
일정 관리 관련 도구
"""
from langchain_core.tools import tool

import requests

@tool
def get_schedule():
    """스케쥴 조회"""
    url = "http://localhost:8800/schedule"
    headers = {"accept": "application/json"}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        return response.json() 
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return None