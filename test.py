from O365 import Account, MSGraphProtocol
from dotenv import load_dotenv
import os

# Load credentials from .env
load_dotenv()
credentials = (
    os.getenv("CLIENT_ID"),
    os.getenv("CLIENT_SECRET")
)

protocol = MSGraphProtocol(default_resource='me')
account = Account(credentials, protocol=protocol)

if not account.is_authenticated:
    raise RuntimeError("❌ Token not found. Re-run auth_once.py.")

# Create a draft
mailbox = account.mailbox()
msg = mailbox.new_message()
msg.to.add("your-email@example.com")  # replace with any valid test email
msg.subject = "Test draft from agent"
msg.body = "This is a test draft email created using the O365 library."

msg.save_draft()
print("✅ Draft created successfully!")
