# tools/rewrite_tool.py

from langchain_ollama import ChatOllama
from langchain_core.tools import tool
import json, re

@tool
def composeEmail(raw: str, recipient_name: str = "") -> dict:
    """
    Rewrites slang or casual input into a professional email.
    Returns a dictionary with 'subject' and 'body'.
    """
    llm = ChatOllama(model="llama3.2:3b", temperature=0)

    prompt = (
        "Rewrite the user's input as a short, professional email. "
        "Keep dates and commitments. Format your response as JSON with keys: subject and body.\n"
        f"recipient_name: {recipient_name}\n"
        f"user_input: {raw}\n\n"
        "JSON:"
    )

    output = llm.invoke(prompt).content

    # Extract JSON block if present (handles ```json fences or inline JSON)
    json_block = None
    fence_match = re.search(r"```json\s*([\s\S]*?)```", output, flags=re.I)
    if fence_match:
        json_block = fence_match.group(1)
    else:
        brace_match = re.search(r"\{[\s\S]*\}$", output.strip())
        if brace_match:
            json_block = brace_match.group(0)

    payload = None
    if json_block:
        try:
            payload = json.loads(json_block)
        except Exception:
            payload = None

    # Fallback: try to parse any JSON-looking content inside the output
    if payload is None:
        try:
            any_match = re.search(r"\{[\s\S]*?\}", output)
            if any_match:
                payload = json.loads(any_match.group(0))
        except Exception:
            payload = None

    # Normalize to clean strings
    subject = "Follow up"
    body = output.strip()

    if isinstance(payload, dict):
        subj_val = payload.get("subject")
        body_val = payload.get("body")

        if isinstance(subj_val, str) and subj_val.strip():
            subject = subj_val.strip()

        # If body is a dict, prefer 'message' field; else stringify
        if isinstance(body_val, dict):
            message_val = body_val.get("message") or body_val.get("text")
            if isinstance(message_val, str) and message_val.strip():
                body = message_val.strip()
            else:
                # Flatten any string fields concatenated
                string_parts = [str(v) for v in body_val.values() if isinstance(v, str)]
                body = "\n".join(string_parts) if string_parts else json.dumps(body_val)
        elif isinstance(body_val, str) and body_val.strip():
            body = body_val.strip()

    # Remove any leftover code fences or notes accidentally included
    body = re.sub(r"```[\s\S]*?```", "", body).strip()

    return {"subject": subject, "body": body}
