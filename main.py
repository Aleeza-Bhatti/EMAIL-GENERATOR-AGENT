# main.py

from agent import build_agent
from langchain_core.messages import HumanMessage

def main():
    print("Welcome to the Email Generator Agent!")
    print("Enter the message you want to convert into a professional email draft.")
    user_input = input("Your message: ")

    agent = build_agent()
    response = agent.invoke(HumanMessage(content=user_input))

    print("\n=== Full Agent Response ===")
    # Print the raw response dict (debugging)
    print(response)

    print("\n=== Parsed Messages ===")
    for msg in response["messages"]:
        print(f"- {msg.type.upper()}")
        print(msg.content)
        print("------")

    print("\n=== Final Answer (if any) ===")
    ai_messages = [msg for msg in response["messages"] if msg.type == "ai"]
    if ai_messages:
        print(ai_messages[-1].content)
    else:
        print("No final AI message returned.")

if __name__ == "__main__":
    main()
