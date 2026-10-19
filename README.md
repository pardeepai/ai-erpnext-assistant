# AI ERPNext Business Assistant

A compact multi-agent assistant that queries ERPNext (customers, contacts, sales orders) using LangGraph workflows and a local LLM. Provides a simple Gradio UI for conversational queries.

Quick start
1. Clone:
   git clone https://github.com/pardeepai/ai-erpnext-assistant.git
   cd ai-erpnext-assistant

2. Virtualenv & deps:
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

3. Environment (.env):
   ERPNEXT_URL=http://127.0.0.1:8000
   ERPNEXT_API_KEY=your_api_key
   ERPNEXT_API_SECRET=your_api_secret
   OLLAMA_URL=http://127.0.0.1:11434
   MODEL_NAME=qwen2.5:3b

4. Run (example):
   python multi_agent_gradio_app.py

What it does
- Retrieve customer details and contacts.
- Fetch sales orders with optional status filtering.
- Multi-agent routing for combined queries.

Testing
- Run tests:
  python -m pytest

Notes
- Requires access to an ERPNext instance and an Ollama-hosted local model.
- Do not commit .env or secrets.

Author
- Pardeep Awasthy — https://github.com/pardeepai
