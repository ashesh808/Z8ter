import { defineConfig } from "vite";
import solid from "vite-plugin-solid";
import path from "node:path";

export default defineConfig({
  plugins: [solid()],
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
