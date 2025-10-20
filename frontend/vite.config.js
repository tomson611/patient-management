import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // when running in docker-compose, target the backend service by name
      '/auth': 'http://app:8001',
      '/patients': 'http://app:8001',
      // add other backend routes as needed
    },
  },
});
