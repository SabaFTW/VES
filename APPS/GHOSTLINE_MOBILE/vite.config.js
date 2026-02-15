import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
    base: './', // Allow relative paths for assets
    plugins: [react()],
    server: {
        host: true, // Allow external access (0.0.0.0)
        port: 5173,
        strictPort: true,
    }
})
