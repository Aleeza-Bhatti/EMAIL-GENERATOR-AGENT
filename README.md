# Email Generator Agent

Turn your notes or voice notes and casual messages into polished emails, no overthinking. Perfect for busy students, club leads, and small business owners who need to follow up fast and sound great doing it.

## What It Does

- Rewrites casual input into a professional email (subject + body)
- Optionally creates an Outlook draft when you include a recipient email

## Local LLMs

The agent uses **Ollama** with the `llama3.2:3b` model. The LLM runs entirely on your machine—no cloud APIs. It rewrites your text into professional email format and decides when to call tools (compose, create draft).

**Setup:**
1. Install [Ollama](https://ollama.com/)
2. Pull the model: `ollama pull llama3.2:3b`
3. Start Ollama (it usually runs as a background service; if not, run `ollama serve`)

## .env (for Outlook drafts)

Copy `.env.example` to `.env` and fill in your Microsoft 365 app credentials:


Get these from an [Azure app registration](https://portal.azure.com/) with Mail.ReadWrite permissions. The LLM works without `.env`; you only need this to create Outlook drafts.

## Usage

```bash
pip install -r requirements.txt
python main.py
```

Include a recipient email in your message if you want an Outlook draft created.

## Project Status
- Input is text only at the moment; voice to text is still in progress
