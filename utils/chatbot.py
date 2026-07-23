from .ai_client import ask_ai
import re

def ask_question(document_text, question):

    prompt = f"""
You are a professional legal assistant.

Here is the legal document:
{document_text}

User Question:
{question}

Answer clearly and only based on the document.

IMPORTANT:
- Do NOT use markdown symbols like ** or *
- Use numbered format if listing points
- Keep formatting clean
"""

    response = ask_ai(prompt)

    # ✅ Remove markdown bold
    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)

    # ✅ Add line break before numbered points
    response = re.sub(r"(\d+\.)", r"\n\1", response)

    # ✅ Remove unwanted label
    response = response.replace("LegalGPT:", "").strip()

    return response