import { useState } from "react";
import { loadDemo, reportUrl, uploadLog } from "./api";
import MetricCard from "./components/MetricCard";
import {
  AttackTimeline,
  CategoryChart,
  StatusChart,
} from "./components/Charts";
import ThreatTable from "./components/ThreatTable";
import "./styles.css";

export default function App() {
  const [job, setJob] = useState(null);
  const [message, setMessage] = useState(
    "Load the demo log or upload an Apache/Nginx access log to begin."
  );
  const [loading, setLoading] = useState(false);

  async function runAnalysis(action) {
    setLoading(true);
    setMessage("Analyzing log stream…");

    try {
      const result = await action();

      console.log("========== SUCCESS ==========");
      console.log(result);
      console.log("=============================");

      setJob(result);

      setMessage(
        result.status === "completed"
          ? "Analysis completed successfully."
          : result.error
      );
    } catch (error) {
      console.log("========== UPLOAD ERROR ==========");
      console.log("Full Error:", error);
      console.log("Response:", error.response);
      console.log("Status:", error.response?.status);
      console.log("Data:", error.response?.data);
      console.log("Message:", error.message);
      console.log("==================================");

      setMessage(
        error.response?.data?.error ||
          error.message ||
          "The analysis could not be completed."
      );
    } finally {
      setLoading(false);
    }
  }

  function handleFileChange(event) {
    const [file] = event.target.files;

    if (file) {
      console.log("Uploading:", file.name);
      runAnalysis(() => uploadLog(file));
    }

    event.target.value = "";
  }

  const threats = job?.threats || [];

  return (
    <main className="app-shell">
      <header>
        <div>
          <p className="eyebrow">SIEM-LITE SECURITY MONITORING</p>
          <h1>LogLens</h1>
          <p className="subtitle">
            Turn web-server access logs into practical security insights.
          </p>
        </div>

        <div className="actions">
          <label className="button primary">
            Upload Log
            <input
              type="file"
              accept=".log,.txt,.access"
              onChange={handleFileChange}
              hidden
            />
          </label>

          <button
            className="button secondary"
            onClick={() => runAnalysis(loadDemo)}
            disabled={loading}
          >
            Load Demo
          </button>
        </div>
      </header>

      <p className={`notice ${job?.status === "failed" ? "error" : ""}`}>
        {loading ? "Analyzing…" : message}
      </p>

      {!job ? (
        <section className="welcome">
          <h2>Ready for an investigation</h2>
          <p>
            The demo contains SQL injection, XSS, directory traversal,
            and brute-force examples.
          </p>
        </section>
      ) : (
        <>
          <section className="metrics">
            <MetricCard
              label="Total Requests"
              value={job.total_requests}
            />

            <MetricCard
              label="Total Threats"
              value={threats.length}
              accent="red"
            />

            <MetricCard
              label="Unique Attackers"
              value={Object.keys(job.top_attackers).length}
              accent="purple"
            />

            <MetricCard
              label="Malformed Lines"
              value={job.malformed_lines}
              accent="orange"
            />
          </section>

          <section className="export-row">
            <span>
              Source: <strong>{job.source_name}</strong>
            </span>

            <div>
              <a
                className="button secondary"
                href={reportUrl(job.id, "csv")}
              >
                Export CSV
              </a>

              <a
                className="button secondary"
                href={reportUrl(job.id, "pdf")}
              >
                Export PDF
              </a>
            </div>
          </section>

          <section className="charts">
            <AttackTimeline data={job.attack_timeline} />
            <CategoryChart data={job.attack_categories} />
            <StatusChart data={job.status_distribution} />
          </section>

          <section className="attackers">
            <h2>Top Attackers</h2>

            {Object.keys(job.top_attackers).length ? (
              Object.entries(job.top_attackers).map(([ip, count]) => (
                <div className="attacker" key={ip}>
                  <code>{ip}</code>
                  <span>{count} events</span>
                </div>
              ))
            ) : (
              <p className="empty">
                No attacker activity detected.
              </p>
            )}
          </section>

          <ThreatTable threats={threats} />
        </>
      )}
    </main>
  );
}