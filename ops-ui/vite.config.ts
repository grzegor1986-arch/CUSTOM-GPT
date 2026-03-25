import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    port: 4173,
    proxy: {
      '/api': {
        target: process.env.ORCHESTRATOR_URL ?? 'http://localhost:8080',
        changeOrigin: true
      }
    }
  }
});
