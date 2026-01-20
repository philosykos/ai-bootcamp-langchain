"""
Cafeteria Agent - 구내식당 메뉴 관리
"""
from typing import Literal, TYPE_CHECKING
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode

from config.settings import get_llm
from tools.cafeteria import get_cafeteria_menu

if TYPE_CHECKING:
    from core.state import State

llm = get_llm()

# Tool을 LLM에 바인딩
cafeteria_tools = [get_cafeteria_menu]
llm_with_tools = llm.bind_tools(cafeteria_tools)

# Cafeteria Agent 시스템 메시지
CAFETERIA_SYSTEM_MESSAGE = "당신은 구내식당을 관리하는 영양사입니다. 사용자에게 이번 주의 식단을 알려줄 수 있습니다."

def cafeteria_agent_func(state: MessagesState):
    """Cafeteria Agent의 핵심 로직"""
    messages = [SystemMessage(content=CAFETERIA_SYSTEM_MESSAGE)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState):
    """도구 호출이 필요한지 확인"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# Cafeteria Agent 그래프 생성
def create_cafeteria_graph():
    """Cafeteria Agent의 내부 그래프"""
    workflow = StateGraph(MessagesState)
    
    workflow.add_node("agent", cafeteria_agent_func)
    workflow.add_node("tools", ToolNode(cafeteria_tools))
    
    workflow.add_edge(START, "agent")
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    workflow.add_edge("tools", "agent")
    
    return workflow.compile()

cafeteria_graph = create_cafeteria_graph()

def cafeteria_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    """구내식당 Agent 실행"""
    print("\n🍽️ Cafeteria Agent 실행 중...")
    
    result = cafeteria_graph.invoke(state)
    
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="cafeteria")
            ]
        },
        goto="supervisor",
    )