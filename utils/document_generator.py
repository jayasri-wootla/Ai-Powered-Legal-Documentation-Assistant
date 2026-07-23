from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from io import BytesIO
from utils.ai_client import ask_ai
import re


def generate_document(doc_type, details):

    prompt = f"""
    Draft a professional and legally structured {doc_type}.
    
    Requirements:
    - Use proper headings
    - Use numbered clauses
    - Use formal legal language
    - Include standard terms and conditions
    - Do NOT use markdown symbols like ** or *
    
    Details:
    {details}
    """

    generated_text = ask_ai(prompt)

    # ✅ Remove markdown formatting
    generated_text = re.sub(r"\*\*(.*?)\*\*", r"\1", generated_text)
    generated_text = re.sub(r"\*(.*?)\*", r"\1", generated_text)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    left_margin = 40
    right_margin = 40
    usable_width = width - left_margin - right_margin

    y = height - 40
    pdf.setFont("Helvetica", 11)

    for paragraph in generated_text.split("\n"):

        # ✅ Wrap text properly
        wrapped_lines = simpleSplit(paragraph, "Helvetica", 11, usable_width)

        for line in wrapped_lines:
            pdf.drawString(left_margin, y, line)
            y -= 15

            if y < 40:
                pdf.showPage()
                pdf.setFont("Helvetica", 11)
                y = height - 40

        y -= 5  # small gap after paragraph

    pdf.save()
    buffer.seek(0)

    return buffer