from pathlib import Path

from app import create_app


def test_demo_endpoint_returns_completed_job(tmp_path):
    demo = tmp_path / "demo.log"
    demo.write_text('127.0.0.1 - - [10/Oct/2025:13:55:36 +0000] "GET / HTTP/1.1" 200 10\n')
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": tmp_path, "DEMO_LOG": demo})
    response = app.test_client().post("/demo")
    assert response.status_code == 201
    assert response.json["status"] == "completed"


def test_upload_rejects_unsupported_extension(tmp_path):
    app = create_app({"TESTING": True, "UPLOAD_FOLDER": tmp_path})
    response = app.test_client().post("/uploads", data={"file": (Path(__file__), "bad.exe")})
    assert response.status_code == 415
