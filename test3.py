from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

def test_chat():
    llm = ChatOllama(model="llama3.2:3b", temperature=0)
    response = llm.invoke([
        SystemMessage(content=(
            "You are an agent that must always follow the ReAct format.\n"
            "When reasoning, use this exact style:\n"
            "Thought: <your reasoning>\n"
            "Action: <the tool name>\n"
            "Action Input: <the tool input as JSON>\n"
            "Observation: <the tool result>\n"
            "Final Answer: <your final reply to the user>\n\n"
            "If the user is just chatting (like saying hi), respond directly as Bob and end the conversation.\n"
            "You help users create professional email drafts from informal or slang messages.\n"
            "Always call the `composeEmail` tool first to rewrite the input.\n"
            "Then call `o365_create_draft` using the rewritten subject and body.\n"
            "Never send the email — only create a draft."
        )),
        HumanMessage(content="yo boss i am going to be late")
    ])
    print("Direct Chat Response:", response.content)

if __name__ == "__main__":
    test_chat()
