from .ai_client import ask_ai
import re

def detect_clauses(text):

    prompt = f"""
You are a legal expert.

Read the contract and list all major clauses present.

For each clause:
- Provide the clause name
- Provide a short explanation (1-2 sentences)

Use numbered format like:

1. Rent Clause: Explanation
2. Termination Clause: Explanation

Return plain text only.
Do NOT return JSON.
Do NOT use markdown symbols like **.

Contract:
{text}
"""

    response = ask_ai(prompt)

    # ✅ Remove markdown bold
    response = re.sub(r"\*\*(.*?)\*\*", r"\1", response)

    # ✅ Remove leading blank lines
    response = response.lstrip()

    # ✅ Ensure numbering starts correctly on new lines
    response = re.sub(r"(?<!^)\s*(\d+\.)", r"\n\1", response)

    # ✅ Remove extra blank lines
    response = re.sub(r"\n\s*\n+", "\n", response)

    # ✅ Fix broken numbers like 18,\n000
    response = re.sub(r",\s*\n\s*", ",", response)

    return response.strip()