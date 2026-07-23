from .ai_client import ask_ai
import re

def suggest_improvements(contract_text):

    prompt = f"""
You are a professional legal consultant.

Review the following contract and suggest 4 to 6 practical improvements 
to make it legally stronger and reduce potential risks.

Each suggestion should:
- Be clear and actionable
- Be written in simple professional language
- Do NOT use markdown symbols like ** or *

Return plain text only.

Contract:
{contract_text}
"""

    response = ask_ai(prompt)

    # ✅ Remove markdown bold formatting
    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)

    return response