import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Enable Vite's React and JSX/TSX support.
export default defineConfig({
  plugins: [react()],
})
