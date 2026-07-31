import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const COLORS = [
  "#3B82F6",
  "#EF4444",
  "#F59E0B",
  "#10B981",
  "#8B5CF6",
  "#EC4899",
];

function toData(record, label = "name") {
  return Object.entries(record || {}).map(([key, value]) => ({
    [label]: key,
    value,
  }));
}

/* ============================
   Attack Timeline
============================ */

export function AttackTimeline({ data }) {
  const chartData = toData(data, "time").map((item) => ({
    ...item,
    time:
      item.time.length > 16
        ? item.time.substring(11, 16)
        : item.time,
  }));

  return (
    <section className="chart-card wide">
      <h2>Attack Timeline</h2>

      <ResponsiveContainer width="100%" height={300}>
        <AreaChart data={chartData}>
          <defs>
            <linearGradient id="threatFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#EF4444" stopOpacity={0.7} />
              <stop offset="95%" stopColor="#EF4444" stopOpacity={0.05} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="4 4" stroke="#334155" />

          <XAxis
            dataKey="time"
            tick={{ fill: "#CBD5E1", fontSize: 11 }}
            interval="preserveStartEnd"
          />

          <YAxis
            allowDecimals={false}
            tick={{ fill: "#CBD5E1" }}
          />

          <Tooltip />

          <Area
            type="monotone"
            dataKey="value"
            stroke="#EF4444"
            strokeWidth={3}
            fill="url(#threatFill)"
            name="Threats"
          />
        </AreaChart>
      </ResponsiveContainer>
    </section>
  );
}

/* ============================
   Attack Categories
============================ */

export function CategoryChart({ data }) {
  const chartData = toData(data);

  return (
    <section className="chart-card">
      <h2>Attack Categories</h2>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={chartData}
            dataKey="value"
            nameKey="name"
            innerRadius={55}
            outerRadius={95}
            paddingAngle={3}
          >
            {chartData.map((item, index) => (
              <Cell
                key={item.name}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>

          <Legend />

          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </section>
  );
}

/* ============================
   HTTP Status
============================ */

export function StatusChart({ data }) {
  const chartData = toData(data, "status");

  return (
    <section className="chart-card">
      <h2>HTTP Status Codes</h2>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart
          data={chartData}
          layout="vertical"
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />

          <XAxis
            type="number"
            allowDecimals={false}
            tick={{ fill: "#CBD5E1" }}
          />

          <YAxis
            dataKey="status"
            type="category"
            tick={{ fill: "#CBD5E1" }}
          />

          <Tooltip />

          <Bar
            dataKey="value"
            radius={[0, 8, 8, 0]}
          >
            {chartData.map((item, index) => {
              let color = "#38BDF8";

              if (item.status.startsWith("2"))
                color = "#22C55E";
              else if (item.status.startsWith("3"))
                color = "#FACC15";
              else if (item.status.startsWith("4"))
                color = "#F97316";
              else if (item.status.startsWith("5"))
                color = "#EF4444";

              return (
                <Cell
                  key={index}
                  fill={color}
                />
              );
            })}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </section>
  );
}