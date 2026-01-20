"""
나만의 Multi-Agent 만들기
"""
from langchain_core.messages import HumanMessage

from core.workflow import create_graph

# 그래프 생성
graph = create_graph()

# ============================================================
# 실행 함수
# ============================================================

def run_agent(user_input: str):
    """멀티 에이전트 시스템을 실행하고 결과를 반환합니다.
    
    Args:
        user_input: 사용자 입력 메시지
        
    Returns:
        Agent의 최종 응답
    """
    print("\n" + "=" * 70)
    print(f"👤 User: {user_input}")
    print("=" * 70)
    
    # 그래프 실행
    result = graph.invoke({
        "messages": [HumanMessage(content=user_input)]
    })
    
    # 최종 응답 추출
    final_messages = result["messages"]
    
    # Agent가 작성한 최종 응답 찾기
    for msg in reversed(final_messages):
        if isinstance(msg, HumanMessage) and hasattr(msg, 'name'):
            print("\n" + "=" * 70)
            print(f"🤖 {msg.name.upper()} Agent 응답:")
            print(f"{msg.content}")
            print("=" * 70)
            return msg.content
    
    # HumanMessage가 없으면 마지막 메시지 출력
    if final_messages:
        last_msg = final_messages[-1]
        content = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)
        print("\n" + "=" * 70)
        print(f"🤖 Assistant 응답:")
        print(f"{content}")
        print("=" * 70)
        return content
    
    return "응답을 생성할 수 없습니다."

def interactive_mode():
    """사용자와 대화형 모드로 실행합니다."""
    print("\n" + "=" * 70)
    print("🤖 멀티 에이전트 시스템 대화형 모드")
    print("=" * 70)
    print("사용 가능한 명령:")
    print("  - 'exit' 또는 'quit': 종료")
    print("  - 'help': 도움말")
    print("=" * 70)
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['exit', 'quit', '종료']:
                print("\n👋 시스템을 종료합니다.")
                break
            
            if user_input.lower() == 'help':
                print("\n도움말:")
                print("  - 구내식당 메뉴 관련 질문: '오늘 점심 메뉴 뭐야?', '이번주 식단 알려줘'")
                print("  - 일정 관련 질문: '오늘 일정 뭐야?', '내일 뭐 있어?'")
                continue
            
            run_agent(user_input)
            
        except KeyboardInterrupt:
            print("\n\n👋 시스템을 종료합니다.")
            break
        except Exception as e:
            print(f"\n❌ 오류 발생: {e}")

def test_mode():
    """미리 정의된 테스트 케이스를 실행합니다."""
    test_cases = [
        "오늘 점심 메뉴 뭐야?",
        "내일 일정 알려줘",
        "이번주 수요일 식단이 궁금해",
        "오늘 남은 일정 있어?",
    ]
    
    print("\n📝 테스트 모드 시작\n")
    
    for query in test_cases:
        try:
            run_agent(query)
            print("\n" + "-" * 70 + "\n")
        except Exception as e:
            print(f"❌ 에러 발생: {e}")
            import traceback
            traceback.print_exc()
    
    print("\n✅ 모든 테스트 완료!")

def main():
    """메인 함수"""
    print("\n🚀 나만의 Multi-Agent")
    print()
    
    # 실행 모드 선택
    print("실행 모드를 선택하세요:")
    print("  1. 테스트 모드 (미리 정의된 질문)")
    print("  2. 대화형 모드 (직접 질문 입력)")
    
    choice = input("\n선택 (1 또는 2): ").strip()
    
    if choice == "2":
        interactive_mode()
    else:
        test_mode()
        
        # 대화형 모드로 전환 옵션
        cont = input("\n대화형 모드로 전환하시겠습니까? (y/n): ").strip().lower()
        if cont == 'y':
            interactive_mode()

if __name__ == "__main__":
    main()