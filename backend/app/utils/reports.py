"""CSV and PDF report builders for completed analysis jobs."""

import csv
from io import BytesIO, StringIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.models.job import AnalysisJob


CSV_COLUMNS = ["type", "severity", "description", "ip", "timestamp", "path"]


def build_csv_report(job: AnalysisJob) -> StringIO:
    """Build a CSV stream containing the job's detected threats."""
    output = StringIO(newline="")
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
    writer.writeheader()
    writer.writerows(job.threats)
    output.seek(0)
    return output


def build_pdf_report(job: AnalysisJob) -> BytesIO:
    """Build a compact PDF summary and threat-event table."""
    output = BytesIO()
    document = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    content = [
        Paragraph("LogLens Security Analysis Report", styles["Title"]),
        Spacer(1, 12),
        Paragraph(f"Source: {job.source_name}", styles["BodyText"]),
        Paragraph(f"Total requests: {job.total_requests}", styles["BodyText"]),
        Paragraph(f"Threats detected: {len(job.threats)}", styles["BodyText"]),
        Spacer(1, 12),
    ]
    rows = [["Type", "Severity", "IP", "Timestamp", "Path"]]
    for threat in job.threats:
        rows.append([
            threat["type"], threat["severity"], threat["ip"],
            threat["timestamp"], threat["path"][:42],
        ])
    table = Table(rows, repeatRows=1, colWidths=[85, 50, 80, 130, 160])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.lightgrey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
    ]))
    content.append(table)
    document.build(content)
    output.seek(0)
    return output
