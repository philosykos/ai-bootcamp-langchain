"""
Schedule Agent - 일정 관리
"""
from typing import Literal, TYPE_CHECKING
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.types import Command
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode

from config.settings import get_llm
from tools.schedule import get_schedule

if TYPE_CHECKING:
    from core.state import State

llm = get_llm()

# Tool을 LLM에 바인딩
schedule_tools = [get_schedule]
llm_with_tools = llm.bind_tools(schedule_tools)

# Schedule Agent 시스템 메시지
SCHEDULE_SYSTEM_MESSAGE = "당신은 사용자의 일정을 관리하는 비서입니다. 사용자에게 현재 남아있는 일정을 안내합니다."

def schedule_agent_func(state: MessagesState):
    """Schedule Agent의 핵심 로직"""
    messages = [SystemMessage(content=SCHEDULE_SYSTEM_MESSAGE)] + state["messages"]
    response = llm_with_tools.invoke(messages)
    return {"messages": [response]}

def should_continue(state: MessagesState):
    """도구 호출이 필요한지 확인"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "end"

# Schedule Agent 그래프 생성
def create_schedule_graph():
    """Schedule Agent의 내부 그래프"""
    workflow = StateGraph(MessagesState)
    
    workflow.add_node("agent", schedule_agent_func)
    workflow.add_node("tools", ToolNode(schedule_tools))
    
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

schedule_graph = create_schedule_graph()

def schedule_node(state: MessagesState) -> Command[Literal["supervisor"]]:
    """일정 관리 Agent 실행"""
    print("\n📅 Schedule Agent 실행 중...")
    
    result = schedule_graph.invoke(state)
    
    return Command(
        update={
            "messages": [
                HumanMessage(content=result["messages"][-1].content, name="schedule")
            ]
        },
        goto="supervisor",
    )