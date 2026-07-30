"""Upload and demo-analysis endpoints."""

from pathlib import Path

from flask import Blueprint, current_app, jsonify, request
from werkzeug.utils import secure_filename

from app.utils.analyzer import analyze_log_file
from app.utils.job_store import job_store


analysis_blueprint = Blueprint("analysis", __name__)
ALLOWED_EXTENSIONS = {".log", ".txt", ".access"}


def _run_analysis(file_path: Path, source_name: str):
    """Run, persist, and serialize one analysis request."""
    job = analyze_log_file(file_path, source_name, current_app.config)
    job_store.save(job)
    status_code = 201 if job.status == "completed" else 422
    return jsonify(job.to_dict()), status_code


@analysis_blueprint.post("/uploads")
def upload_log():
    """Save a user upload and analyse it without loading it into RAM."""
    if "file" not in request.files:
        return jsonify({"error": "Missing file field."}), 400
    uploaded_file = request.files["file"]
    if not uploaded_file.filename:
        return jsonify({"error": "No file selected."}), 400

    filename = secure_filename(uploaded_file.filename)
    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        return jsonify({"error": "Unsupported file type. Upload a .log, .txt, or .access file."}), 415

    destination = Path(current_app.config["UPLOAD_FOLDER"]) / filename
    uploaded_file.save(destination)
    return _run_analysis(destination, filename)


@analysis_blueprint.post("/demo")
def load_demo():
    """Analyse the bundled sample access log."""
    demo_path = Path(current_app.config["DEMO_LOG"])
    if not demo_path.is_file():
        return jsonify({"error": "Demo log is unavailable."}), 500
    return _run_analysis(demo_path, "demo_access.log")
