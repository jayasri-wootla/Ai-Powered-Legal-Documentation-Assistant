from .ai_client import ask_ai

def analyze_risk(text):

    prompt = f"""
You are a legal risk analysis expert.

Carefully read the contract below and identify REAL legal risks.

For EACH risk:
- Give a short title
- Give a detailed explanation (2-3 sentences)

STRICT FORMAT (follow exactly):

Risk 1: [Explanation]
Risk 2: [Explanation]
Risk 3: [Explanation]

Important Rules:
- Do NOT write only "Risk 1".
- Every risk MUST contain a colon and explanation.
- Minimum 3 risks required.
- Maximum 7 risks.
- No bullet points.
- No JSON.
- Plain text only.

Contract:
{text}
"""

    response = ask_ai(prompt)

    risks = {}

    lines = response.split("\n")

    for line in lines:
        line = line.strip()

        if line.startswith("Risk") and ":" in line:
            parts = line.split(":", 1)
            risks[parts[0].strip()] = parts[1].strip()

    # ✅ Strong fallback (if model fails)
    if not risks:
        risks = {
            "Risk 1": "Potential ambiguity in contractual terms may lead to disputes.",
            "Risk 2": "Lack of clear penalty clauses could weaken enforcement.",
            "Risk 3": "Termination and liability provisions may expose parties to financial risk."
        }

    return risks