import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Enable Vite's React and JSX/TSX support.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/scanLan": "http://127.0.0.1:8000",
      "/scanPorts": "http://127.0.0.1:8000",
      "/scanSpecificPort": "http://127.0.0.1:8000",
      "/showDevices": "http://127.0.0.1:8000",
    },
  },
})
