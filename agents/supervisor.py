"""
Supervisor Agent - 작업자를 관리하고 라우팅
"""
from typing import Literal
from langgraph.graph import END
from langgraph.types import Command

from config.settings import get_llm
from core.state import State, Router, SUPERVISOR_SYSTEM_PROMPT, AGENT_MEMBERS

llm = get_llm()

def supervisor_node(state: State) -> Command[Literal[*AGENT_MEMBERS, "__end__"]]:
    """Supervisor가 다음 작업자를 결정"""
    print("\n👔 Supervisor: 다음 작업자 결정 중...")
    
    messages = [
        {"role": "system", "content": SUPERVISOR_SYSTEM_PROMPT},
    ] + state["messages"]
    
    response = llm.with_structured_output(Router).invoke(messages)
    goto = response["next"]
    
    print(f"   ➜ 결정: {goto}")
    
    if goto == "FINISH":
        goto = END
    
    return Command(goto=goto, update={"next": goto})