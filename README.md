# LangGraph 실습 - 나만의 Multi Agent 만들기

LangGraph를 활용한 나만의 Multi Agent 시스템 만들기

## 📁 프로젝트 구조

```
ai-bootcamp/
├── .env                        # 환경 변수
├── .gitignore                 
├── requirements.txt           
├── README.md                  
├── main.py                     # 메인 실행 파일
├── config/                     # 설정
│   ├── __init__.py
│   └── settings.py             # 환경 변수, LLM 설정
├── core/                       # 핵심 비즈니스 로직
│   ├── __init__.py
│   ├── state.py                # State, Router 정의
│   └── workflow.py             # 그래프 생성 로직
├── agents/                     # 에이전트 구현
│   ├── __init__.py
│   ├── supervisor.py           # Supervisor Agent
│   ├── cafeteria_agent.py      # Cafeteria Agent
│   └── schedule_agent.py       # Schedule Agent
├── tools/                      # 도구 정의
│   ├── __init__.py
│   ├── cafeteria.py            # 구내식당 메뉴 조회
│   └── schedule.py             # 일정 조회
└── utils/                      # 유틸리티
    └── __init__.py
```

## 🚀 시작하기

### 1. 환경 설정

```bash
# 가상환경 생성
python -m venv .venv

# 가상환경 활성화 (Windows)
.venv\Scripts\activate

# 가상환경 활성화 (Mac/Linux)
source .venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가:

```env
AOAI_ENDPOINT=https://your-resource.openai.azure.com/
AOAI_API_KEY=your-api-key-here
AOAI_DEPLOY_GPT4O=gpt-4o
```

### 3. 실행

```bash
python main.py
```

## 🎯 기능

### Agent 종류

1. **Supervisor Agent**
   - 사용자 요청을 분석하여 적절한 Worker Agent로 라우팅
   - 작업 완료 여부 판단

2. **Cafeteria Agent**
   - 구내식당 메뉴 조회
   - 도구: `get_cafeteria_menu`

3. **Schedule Agent**
   - 일정 관리 및 조회
   - 도구: `get_schedule`

### 실행 모드

- **테스트 모드**: 미리 정의된 질문으로 테스트
- **대화형 모드**: 실시간으로 질문 입력

## 📝 사용 예시

```python
from core.workflow import create_graph
from langchain_core.messages import HumanMessage

# 그래프 생성
graph = create_graph()

# 실행
result = graph.invoke({
    "messages": [HumanMessage(content="오늘 점심 메뉴 뭐야?")]
})
```

## 🔧 새로운 Agent 추가하기

### 1. Tool 생성 (`tools/new_tool.py`)

```python
from langchain_core.tools import tool

@tool
def new_tool(param: str) -> str:
    """도구 설명"""
    return "결과"
```

### 2. Agent 생성 (`agents/new_agent.py`)

```python
from langgraph.prebuilt import ToolNode
from tools.new_tool import new_tool

# Agent 구현
def new_agent_func(state):
    # 로직
    pass

def new_node(state):
    # 노드 래퍼
    pass
```

### 3. State 업데이트 (`core/state.py`)

```python
AGENT_MEMBERS = ["cafeteria", "schedule", "new_agent"]
```

### 4. Workflow 업데이트 (`core/workflow.py`)

```python
def create_graph():
    builder = StateGraph(State)
    builder.add_node("new_agent", new_node)
    # ...
```

## 📚 의존성

- `langchain` >= 1.0.5
- `langchain-openai` >= 1.1.0
- `langgraph` >= 1.0.3
- `python-dotenv` >= 1.0.0

## 🏗️ 아키텍처

```
User Input
    ↓
Supervisor
    ↓
┌───────┬──────────┐
│       │          │
Cafeteria Schedule ...
│       │          │
└───────┴──────────┘
    ↓
Supervisor
    ↓
Response
```

## 📄 라이선스

MIT License