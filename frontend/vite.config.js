import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/auth': 'http://localhost:8001',
      '/patients': 'http://localhost:8001',
      // add other backend routes as needed
    },
  },
});
