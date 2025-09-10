# tools/outlook_tools.py

from O365 import Account, MSGraphProtocol
from langchain_core.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()

# Get credentials from .env
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


# Create Outlook account object (use the same approach as test.py)
credentials = (CLIENT_ID, CLIENT_SECRET)
protocol = MSGraphProtocol(default_resource="me")
account = Account(credentials, protocol=protocol)

@tool
def o365_create_draft(to: str, subject: str, body_html: str) -> str:
    """
    Creates an Outlook draft email.
    """
    if not account.is_authenticated:
        raise Exception("Outlook account not authenticated. Run the auth flow used in test.py so the token is available.")

    mailbox = account.mailbox()
    message = mailbox.new_message()
    message.to.add(to)
    message.subject = subject
    message.body = body_html  # must be HTML format
    message.save_draft()

    return f"Draft created for {to} with subject '{subject}'"
