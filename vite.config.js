import { defineConfig } from 'vite';

const basePath = process.env.VITE_BASE_PATH || '/';

export default defineConfig({
  // Vite app root for dev/build
  root: 'APP/public',
  // Dynamic base: local build '/', GitHub Pages build '/VES/'
  base: basePath,
  build: {
    outDir: '../../dist',
    emptyOutDir: true,
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild',
    target: 'es2020'
  },
  server: {
    port: 3000,
    host: true,
    open: true,
    cors: true
  },
  preview: {
    port: 4173,
    host: true,
    cors: true
  },
  define: {
    __APP_VERSION__: JSON.stringify('2.3.0'),
    __BUILD_TIME__: JSON.stringify(new Date().toISOString())
  },
  css: {
    postcss: null
  },
  esbuild: {
    drop: ['console', 'debugger']
  }
});
