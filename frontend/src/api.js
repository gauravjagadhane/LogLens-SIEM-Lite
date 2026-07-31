// HTTP helpers for the LogLens Flask API.

import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://localhost:5000",
  timeout: 30000,
});

api.interceptors.request.use((config) => {
  console.log("========== REQUEST ==========");
  console.log(config.method?.toUpperCase(), config.url);
  console.log(config);
  return config;
});

api.interceptors.response.use(
  (response) => {
    console.log("========== RESPONSE ==========");
    console.log(response.status);
    console.log(response.data);
    return response;
  },
  (error) => {
    console.error("========== AXIOS ERROR ==========");
    console.error(error);

    if (error.response) {
      console.error("STATUS:", error.response.status);
      console.error("DATA:", error.response.data);
    }

    if (error.request) {
      console.error("REQUEST:", error.request);
    }

    console.error("MESSAGE:", error.message);

    return Promise.reject(error);
  }
);

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
