"""Flask application factory for LogLens."""

from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

from app.routes.analysis import analysis_blueprint
from app.routes.jobs import jobs_blueprint


def create_app(test_config: dict | None = None) -> Flask:
    """Create and configure the LogLens Flask application."""
    backend_root = Path(__file__).resolve().parents[1]
    workspace_root = backend_root.parent
    app = Flask(__name__)
    app.config.from_mapping(
        UPLOAD_FOLDER=backend_root / "uploads",
        DEMO_LOG=workspace_root / "Sample_logs" / "demo_access.log",
        MAX_CONTENT_LENGTH=500 * 1024 * 1024,
        BRUTE_FORCE_THRESHOLD=5,
        BRUTE_FORCE_WINDOW_SECONDS=300,
    )
    if test_config:
        app.config.update(test_config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    CORS(app)
    app.register_blueprint(analysis_blueprint)
    app.register_blueprint(jobs_blueprint)

    @app.get("/health")
    def health_check():
        """Return a minimal liveness response for local deployment checks."""
        return jsonify({"status": "ok"})

    @app.errorhandler(413)
    def file_too_large(_error):
        """Return a JSON response when Flask rejects an oversized upload."""
        return jsonify({"error": "File is larger than the 100 MB limit."}), 413

    @app.errorhandler(404)
    def not_found(_error):
        """Return JSON for API routes that do not exist."""
        return jsonify({"error": "Route not found."}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        """Avoid exposing server details to API consumers."""
        return jsonify({"error": "An internal server error occurred."}), 500

    return app
