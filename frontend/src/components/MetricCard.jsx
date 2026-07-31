const ICONS = {
  "Total Requests": "🌐",
  "Total Threats": "🚨",
  "Unique Attackers": "🕵️",
  "Malformed Lines": "⚠️",
};

export default function MetricCard({
  label,
  value,
  accent = "blue",
}) {
  return (
    <article className={`metric-card ${accent}`}>
      <div className="metric-top">
        <span className="metric-icon">
          {ICONS[label] || "📊"}
        </span>
      </div>

      <strong>{Number(value).toLocaleString()}</strong>

      <small>{label}</small>
    </article>
  );
}