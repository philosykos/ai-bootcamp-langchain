"""
State 정의 및 Agent 설정
"""
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import MessagesState

# Agent 멤버 설정
AGENT_MEMBERS = ["cafeteria", "schedule"]
AGENT_OPTIONS = AGENT_MEMBERS + ["FINISH"]

# Supervisor 시스템 프롬프트
SUPERVISOR_SYSTEM_PROMPT = (
    "You are a supervisor tasked with managing a conversation between the"
    f" following workers: {AGENT_MEMBERS}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
    "\n\nWorker descriptions:"
    "\n- cafeteria: Handles questions about cafeteria menus and food"
    "\n- schedule: Handles questions about schedules and appointments"
    "\n\nAnalyze the user's question and route to the appropriate worker."
    "\nIf the question is answered or no worker is needed, respond with FINISH."
)

class Router(TypedDict):
    """Worker to route to next. If no workers needed, route to FINISH."""
    next: Literal[*AGENT_OPTIONS]

class State(MessagesState):
    """Agent 간 공유되는 상태"""
    next: str