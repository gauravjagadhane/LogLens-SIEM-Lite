import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const COLORS = ["#38bdf8", "#f97316", "#ef4444", "#a78bfa", "#22c55e"];

function toData(record, label = "name") {
  return Object.entries(record || {}).map(([key, value]) => ({ [label]: key, value }));
}

export function AttackTimeline({ data }) {
  const chartData = toData(data, "time");
  return (
    <section className="chart-card wide">
      <h2>Attack Timeline</h2>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="time" tick={{ fill: "#94a3b8", fontSize: 11 }} />
          <YAxis allowDecimals={false} tick={{ fill: "#94a3b8" }} />
          <Tooltip />
          <Bar dataKey="value" fill="#ef4444" name="Threats" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </section>
  );
}

export function CategoryChart({ data }) {
  const chartData = toData(data);
  return (
    <section className="chart-card">
      <h2>Attack Categories</h2>
      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie data={chartData} dataKey="value" nameKey="name" outerRadius={82} label>
            {chartData.map((item, index) => <Cell key={item.name} fill={COLORS[index % COLORS.length]} />)}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </section>
  );
}

export function StatusChart({ data }) {
  const chartData = toData(data, "status");
  return (
    <section className="chart-card">
      <h2>HTTP Status Distribution</h2>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="status" tick={{ fill: "#94a3b8" }} />
          <YAxis allowDecimals={false} tick={{ fill: "#94a3b8" }} />
          <Tooltip />
          <Bar dataKey="value" fill="#38bdf8" name="Requests" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </section>
  );
}
