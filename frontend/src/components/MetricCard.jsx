import { motion } from "framer-motion";
import {
  FaGlobe,
  FaShieldAlt,
  FaUserSecret,
  FaExclamationTriangle,
} from "react-icons/fa";

const icons = {
  "Total Requests": <FaGlobe />,
  "Total Threats": <FaShieldAlt />,
  "Unique Attackers": <FaUserSecret />,
  "Malformed Lines": <FaExclamationTriangle />,
};

export default function MetricCard({
  label,
  value,
  accent = "blue",
}) {
  return (
    <motion.article
      className={`metric-card ${accent}`}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      whileHover={{
        y: -8,
        scale: 1.03,
      }}
    >
      <div className="metric-icon">
        {icons[label] || <FaGlobe />}
      </div>

      <div className="metric-content">
        <span>{label}</span>

        <strong>
          {Number(value).toLocaleString()}
        </strong>
      </div>
    </motion.article>
  );
}