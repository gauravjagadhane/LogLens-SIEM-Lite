# Sample Logs

This folder contains sample Apache access logs for testing the LogLens application.

The sample log demonstrates:

- Normal web requests
- SQL Injection attack
- Cross-Site Scripting (XSS)
- Directory Traversal attack
- Brute Force login attempts (multiple HTTP 401 responses)

To test:

1. Launch the backend.
2. Launch the frontend.
3. Upload `demo_access.log`.
4. Verify that LogLens detects all supported threats and displays them in the dashboard.