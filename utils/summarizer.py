from .ai_client import ask_ai
import re

def summarize_contract(text):

    prompt = f"""
You are a professional legal assistant.

Summarize the following contract clearly and concisely.

IMPORTANT:
- Do NOT use markdown symbols like ** or *
- Use numbered points if needed
- Keep language simple and professional

Contract:
{text}
"""

    response = ask_ai(prompt)

    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)

    return response