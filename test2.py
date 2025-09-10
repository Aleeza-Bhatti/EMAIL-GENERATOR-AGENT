# test_agent.py

from agent import build_agent
from langchain_core.messages import HumanMessage

def main():
    print("=== ReAct Agent Test ===")
    agent = build_agent()

    # Ask the agent what tools it has available
    test_input = "What tools do you have available? Please list them."
    response = agent.invoke(HumanMessage(content=test_input))

    print("\nFull Raw Response:")
    print(response)

    print("\nParsed Messages:")
    for msg in response["messages"]:
        print(f"{msg.type.upper()}: {msg.content}")

if __name__ == "__main__":
    main()
