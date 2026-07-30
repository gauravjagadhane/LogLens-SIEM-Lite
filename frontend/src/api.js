// HTTP helpers for the LogLens Flask API.

import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000",
});

export async function uploadLog(file) {
  const formData = new FormData();
  formData.append("file", file);
  const response = await api.post("/uploads", formData);
  return response.data;
}

export async function loadDemo() {
  const response = await api.post("/demo");
  return response.data;
}

export function reportUrl(jobId, format) {
  return `${api.defaults.baseURL}/jobs/${jobId}/export/${format}`;
}
