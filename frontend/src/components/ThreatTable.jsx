const severityClass = (severity) =>
  `severity ${(severity || "low").toLowerCase()}`;

export default function ThreatTable({ threats = [] }) {
  return (
    <section className="table-card">
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "18px",
        }}
      >
        <h2 style={{ margin: 0 }}>Threat Events</h2>

        <span
          style={{
            background: "#1e293b",
            color: "#38bdf8",
            padding: "6px 12px",
            borderRadius: "999px",
            fontSize: ".8rem",
            fontWeight: 700,
          }}
        >
          {threats.length} Detected
        </span>
      </div>

      {threats.length === 0 ? (
        <div
          style={{
            textAlign: "center",
            padding: "45px 20px",
            color: "#94a3b8",
          }}
        >
          <h3 style={{ color: "#e2e8f0", marginBottom: "10px" }}>
            ✅ No Threats Detected
          </h3>

          <p>
            Your uploaded log did not contain any suspicious activity.
          </p>
        </div>
      ) : (
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Attack Type</th>
                <th>Severity</th>
                <th>Source IP</th>
                <th>Timestamp</th>
                <th>Request Path</th>
              </tr>
            </thead>

            <tbody>
              {threats.map((threat, index) => (
                <tr
                  key={`${threat.ip}-${threat.timestamp}-${index}`}
                >
                  <td
                    style={{
                      fontWeight: 600,
                      color: "#f8fafc",
                    }}
                  >
                    {threat.type}
                  </td>

                  <td>
                    <span className={severityClass(threat.severity)}>
                      {threat.severity}
                    </span>
                  </td>

                  <td>
                    <code
                      style={{
                        color: "#38bdf8",
                        fontSize: ".85rem",
                      }}
                    >
                      {threat.ip}
                    </code>
                  </td>

                  <td
                    style={{
                      whiteSpace: "nowrap",
                      color: "#cbd5e1",
                    }}
                  >
                    {threat.timestamp}
                  </td>

                  <td className="path">
                    {threat.path}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}