const severityClass = (severity) => `severity ${severity.toLowerCase()}`;

export default function ThreatTable({ threats = [] }) {
  return (
    <section className="table-card">
      <h2>Threat Events</h2>
      {threats.length === 0 ? <p className="empty">No threats were detected in this log.</p> : (
        <div className="table-wrap">
          <table>
            <thead><tr><th>Type</th><th>Severity</th><th>Source IP</th><th>Timestamp</th><th>Path</th></tr></thead>
            <tbody>
              {threats.map((threat, index) => (
                <tr key={`${threat.ip}-${threat.timestamp}-${index}`}>
                  <td>{threat.type}</td><td><span className={severityClass(threat.severity)}>{threat.severity}</span></td>
                  <td>{threat.ip}</td><td>{threat.timestamp}</td><td className="path">{threat.path}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
