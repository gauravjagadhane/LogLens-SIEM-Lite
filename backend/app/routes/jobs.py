"""Job retrieval and report-download endpoints."""

from flask import Blueprint, jsonify, send_file

from app.utils.job_store import job_store
from app.utils.reports import build_csv_report, build_pdf_report


jobs_blueprint = Blueprint("jobs", __name__)


def _get_job_or_404(job_id: str):
    """Return a stored job or a standard JSON 404 response."""
    job = job_store.get(job_id)
    if job is None:
        return None, (jsonify({"error": "Analysis job not found."}), 404)
    return job, None


@jobs_blueprint.get("/jobs/<job_id>")
def get_job(job_id: str):
    """Return all dashboard data for a completed analysis."""
    job, error_response = _get_job_or_404(job_id)
    if error_response:
        return error_response
    return jsonify(job.to_dict())


@jobs_blueprint.get("/jobs/<job_id>/export/csv")
def export_csv(job_id: str):
    """Download detected threats as a CSV file."""
    job, error_response = _get_job_or_404(job_id)
    if error_response:
        return error_response
    return send_file(build_csv_report(job), mimetype="text/csv", as_attachment=True,
                     download_name=f"loglens-{job_id}.csv")


@jobs_blueprint.get("/jobs/<job_id>/export/pdf")
def export_pdf(job_id: str):
    """Download a presentation-ready PDF threat report."""
    job, error_response = _get_job_or_404(job_id)
    if error_response:
        return error_response
    return send_file(build_pdf_report(job), mimetype="application/pdf", as_attachment=True,
                     download_name=f"loglens-{job_id}.pdf")
