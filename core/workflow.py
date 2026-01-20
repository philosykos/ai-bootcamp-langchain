"""
LangGraph 워크플로우 구성
"""
from langgraph.graph import StateGraph, START

from core.state import State
from agents.supervisor import supervisor_node
from agents.cafeteria_agent import cafeteria_node
from agents.schedule_agent import schedule_node

def create_graph():
    """멀티 에이전트 그래프를 생성하고 컴파일합니다.
    
    Returns:
        컴파일된 StateGraph 인스턴스
    """
    builder = StateGraph(State)
    
    # 노드 추가
    builder.add_node("supervisor", supervisor_node)
    builder.add_node("cafeteria", cafeteria_node)
    builder.add_node("schedule", schedule_node)
    
    # 엣지 추가
    builder.add_edge(START, "supervisor")
    
    # 그래프 컴파일
    graph = builder.compile()
    
    return graph