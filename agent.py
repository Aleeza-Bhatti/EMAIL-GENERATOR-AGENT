# agent.py

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
import json
import re

# Import your tools
from tools.composeEmail import composeEmail
from tools.outlookTools import o365_create_draft

class SimpleEmailAgent:
    
    def __init__(self):
        self.llm = ChatOllama(model="llama3.2:3b", temperature=0)
        self.tools = {
            "composeEmail": composeEmail,
            "o365_create_draft": o365_create_draft
        }
    
    def invoke(self, message):
        if isinstance(message, HumanMessage):
            user_input = message.content
        else:
            user_input = str(message)
        
        # System prompt
        system_prompt = (
            "You are a helpful assistant that creates professional email drafts.\n"
            "You MUST follow this exact format:\n"
            "Thought: <your reasoning>\n"
            "Action: <tool name>\n"
            "Action Input: <JSON input>\n"
            "Observation: <tool result>\n"
            "Final Answer: <your response>\n\n"
            "Available tools:\n"
            "- composeEmail: Takes {'raw': 'text', 'recipient_name': 'name'}\n"
            "- o365_create_draft: Takes {'to': 'email', 'subject': 'subject', 'body_html': 'body'}\n\n"
            "If the user just says 'hi' or similar greetings, respond with a friendly greeting and ask what email they'd like to create.\n"
            "For email requests, ALWAYS call composeEmail first, then o365_create_draft."
        )
        
        # Get initial response
        response = self.llm.invoke([
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ])
        
        # Parse the response and execute tools if needed
        content = response.content
        
        # Check if we need to call tools
        if "Action:" in content and "Action Input:" in content:
            # Extract action and input
            action_match = re.search(r"Action:\s*(\w+)", content)
            input_match = re.search(r"Action Input:\s*(.+)", content)
            
            if action_match and input_match:
                action = action_match.group(1)
                action_input_str = input_match.group(1).strip()
                
                # Try to parse JSON input
                try:
                    action_input = json.loads(action_input_str)
                except Exception as e:
                    # If not JSON, create a simple dict
                    action_input = {"raw": action_input_str}
                
                # Execute the tool
                if action in self.tools:
                    try:
                        tool_result = self.tools[action].invoke(action_input)
                        
                        # Create a simple final response
                        if action == "composeEmail":
                            # Extract recipient email from the user's input, if present
                            recipient_match = re.search(r"[\w\.-]+@[\w\.-]+\.[A-Za-z]{2,}", user_input)
                            recipient_email = recipient_match.group(0) if recipient_match else None

                            subject = tool_result.get('subject', 'Email')
                            body_text = tool_result.get('body', '')
                            # Convert to simple HTML
                            body_html = "<p>" + body_text.replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>"

                            if recipient_email:
                                try:
                                    draft_result = self.tools["o365_create_draft"].invoke({
                                        "to": recipient_email,
                                        "subject": subject,
                                        "body_html": body_html
                                    })
                                    content = f"Draft created: {draft_result}"
                                except Exception as e:
                                    content = (
                                        f"I prepared your email but could not create the Outlook draft: {str(e)}\n\n"
                                        f"Subject: {subject}\n\nBody:\n{body_text}\n\n"
                                        f"You can retry after authenticating Outlook, or share credentials."
                                    )
                            else:
                                content = (
                                    f"I've rewritten your message into a professional email, but I didn't find a recipient email address in your request.\n\n"
                                    f"Subject: {subject}\n\nBody:\n{body_text}\n\n"
                                    f"Please provide a recipient email (e.g., name@example.com) to create the Outlook draft."
                                )
                        else:
                            content = f"Tool executed successfully: {tool_result}"
                    except Exception as e:
                        content = f"Error executing tool: {str(e)}"
        
        # Return in the expected format
        from langchain_core.messages import AIMessage
        return {"messages": [AIMessage(content=content)]}

def build_agent():
    return SimpleEmailAgent()
