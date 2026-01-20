"""
구내식당 관련 도구
"""
from langchain_core.tools import tool

import requests

@tool
def get_cafeteria_menu(day: str|None):
    """
    주어진 요일의 구내식당 메뉴를 조회하는 함수.
    day 가 None 일 경우 이번주 메뉴 조회

    :param day: 조회할 요일 (예: '월요일', '화요일' 등)
    :return: JSON 응답을 파이썬 딕셔너리로 변환하여 반환
    """
    url = "http://localhost:8800/cafeteria-menu"
    params = {"day": day}
    headers = {"accept": "application/json"}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 발생
        return response.json()  # JSON 응답을 파이썬 딕셔너리로 변환
    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류 발생: {e}")
        return None