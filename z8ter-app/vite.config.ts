import path from "node:path";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react()],
  appType: "custom",
  base: "/static/js",
  build: {
    outDir: "static/js",
    assetsDir: "assets",
    sourcemap: true,
    manifest: true,
    rollupOptions: {
      input: path.resolve(__dirname, "src/ts/app.ts"),
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src/ts")
    },
  },
});
