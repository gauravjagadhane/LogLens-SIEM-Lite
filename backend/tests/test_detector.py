from pathlib import Path

from app.detector.threat_detector import ThreatDetector


def make_detector():
    return ThreatDetector(Path(__file__).parents[1] / "app" / "detector" / "signatures.json", 3, 300)


def event(path, status=200, timestamp="10/Oct/2025:13:55:36 +0000"):
    return {"ip": "10.0.0.1", "timestamp": timestamp, "method": "GET", "path": path,
            "protocol": "HTTP/1.1", "status": status, "size": 0, "user_agent": ""}


def test_detects_sql_injection():
    detections = list(make_detector().inspect(event("/search?q=1%20UNION%20SELECT%20password")))
    assert detections[0]["type"] == "SQL Injection"


def test_detects_brute_force_after_threshold():
    detector = make_detector()
    results = [list(detector.inspect(event("/login", 401, f"10/Oct/2025:13:5{i}:00 +0000"))) for i in range(3)]
    assert results[-1][0]["type"] == "Brute Force"
