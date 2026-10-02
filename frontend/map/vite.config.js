import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";

// /api/* is forwarded to Vinit's FastAPI backend (Task 3).
// e.g. fetch("/api/requests")  ->  http://localhost:8000/requests
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  return {
    plugins: [react()],
    server: {
      port: 5173,
      host: true, // lets teammates / ngrok reach the dev server
      proxy: {
        "/api": {
          target: env.VITE_BACKEND_URL || "http://localhost:8000",
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ""),
        },
      },
    },
  };
});
