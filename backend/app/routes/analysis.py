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

    print("\n" + "=" * 70)
    print("🚀 UPLOAD ROUTE HIT")
    print("=" * 70)

    print("Method:", request.method)
    print("Headers:", dict(request.headers))
    print("Files:", request.files)

    if "file" not in request.files:
        print("❌ ERROR: Missing file field.")
        return jsonify({"error": "Missing file field."}), 400

    uploaded_file = request.files["file"]

    print("Filename:", uploaded_file.filename)

    if not uploaded_file.filename:
        print("❌ ERROR: No filename.")
        return jsonify({"error": "No file selected."}), 400

    filename = secure_filename(uploaded_file.filename)

    print("Secure filename:", filename)

    if Path(filename).suffix.lower() not in ALLOWED_EXTENSIONS:
        print("❌ ERROR: Unsupported extension:", Path(filename).suffix)
        return jsonify(
            {
                "error": "Unsupported file type. Upload a .log, .txt, or .access file."
            }
        ), 415

    destination = Path(current_app.config["UPLOAD_FOLDER"]) / filename

    print("Saving to:", destination)

    try:
        uploaded_file.save(destination)
        print("✅ File saved successfully.")
    except Exception as e:
        print("❌ Failed to save file.")
        print(e)
        return jsonify({"error": str(e)}), 500

    try:
        print("Starting analysis...")

        result = _run_analysis(destination, filename)

        print("✅ Analysis completed.")
        print("=" * 70)

        return result

    except Exception as e:
        import traceback

        print("❌ ANALYSIS CRASHED")
        traceback.print_exc()

        return jsonify(
            {
                "error": str(e),
                "traceback": traceback.format_exc(),
            }
        ), 500


@analysis_blueprint.post("/demo")
def load_demo():
    """Analyse the bundled sample access log."""

    print("🚀 DEMO ROUTE HIT")

    demo_path = Path(current_app.config["DEMO_LOG"])

    if not demo_path.is_file():
        print("❌ Demo log missing.")
        return jsonify({"error": "Demo log is unavailable."}), 500

    return _run_analysis(demo_path, "demo_access.log")