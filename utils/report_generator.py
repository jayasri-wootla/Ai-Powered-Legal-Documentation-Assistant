from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from utils.improvement_suggester import suggest_improvements
import os
from datetime import datetime
import re


def generate_report(summary, clauses, risks, improvements):

    if not os.path.exists("reports"):
        os.makedirs("reports")

    file_name = f"reports/report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

    c = canvas.Canvas(file_name, pagesize=A4)
    width, height = A4

    left_margin = 50
    right_margin = 50
    usable_width = width - left_margin - right_margin
    y = height - 40

    # ✅ Clean summary markdown/newline issues
    summary = re.sub(r"\*\*(.*?)\*\*", r"\1", summary)
    summary = summary.replace("\\n", "\n")

    # ================= TITLE =================
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left_margin, y, "LegalGPT - Contract Analysis Report")
    y -= 40

    # ================= SUMMARY =================
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_margin, y, "Summary:")
    y -= 20
    c.setFont("Helvetica", 11)

    for paragraph in summary.split("\n"):
        wrapped_lines = simpleSplit(paragraph, "Helvetica", 11, usable_width)

        for line in wrapped_lines:
            c.drawString(left_margin + 10, y, line)
            y -= 15

            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 40

        y -= 5

    # ================= CLAUSES =================
    # ---------------- CLAUSES ----------------
    y -= 15
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_margin, y, "Clause Detection:")
    y -= 20
    c.setFont("Helvetica", 11)

# ✅ Properly format dictionary
    if isinstance(clauses, dict):
        for key, clause in clauses.items():

        # ✅ If nested dictionary structure
            if isinstance(clause, dict):
                title = clause.get("Title", key)
                explanation = clause.get("Explanation", "")
                clause_text = f"{title}: {explanation}"
            else:
                clause_text = f"{key}: {clause}"

            wrapped_lines = simpleSplit(clause_text, "Helvetica", 11, usable_width)

            for line in wrapped_lines:
                c.drawString(left_margin + 10, y, line)
                y -= 15

                if y < 40:
                    c.showPage()
                    c.setFont("Helvetica", 11)
                    y = height - 40

            y -= 8
    else:
    # ✅ If accidentally string passed
        wrapped_lines = simpleSplit(str(clauses), "Helvetica", 11, usable_width)

        for line in wrapped_lines:
            c.drawString(left_margin + 10, y, line)
            y -= 15

            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 40

    # ================= RISKS =================
    y -= 15
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_margin, y, "Risk Analysis:")
    y -= 20
    c.setFont("Helvetica", 11)

    for key, value in risks.items():   # ✅ FIXED HERE
        text = f"{key}: {value}"
        wrapped_lines = simpleSplit(text, "Helvetica", 11, usable_width)

        for line in wrapped_lines:
            c.drawString(left_margin + 10, y, line)
            y -= 15

            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 40

        y -= 5


    # ================= IMPROVEMENTS =================
    y -= 15
    c.setFont("Helvetica-Bold", 13)
    c.drawString(left_margin, y, "AI Suggested Improvements:")
    y -= 20
    c.setFont("Helvetica", 11)


    improvements = re.sub(r"\*\*(.*?)\*\*", r"\1", improvements)

    for paragraph in improvements.split("\n"):
        wrapped_lines = simpleSplit(paragraph, "Helvetica", 11, usable_width)

        for line in wrapped_lines:
            c.drawString(left_margin + 10, y, line)
            y -= 15

            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 11)
                y = height - 40

        y -= 5


    c.save()
    return file_name