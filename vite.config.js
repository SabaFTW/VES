import { defineConfig } from 'vite';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const currentDir = dirname(fileURLToPath(import.meta.url));
const portalRoot = resolve(currentDir, 'APP/public');

export default defineConfig(({ mode }) => {
  const isGithubPages = mode === 'github-pages';

  return {
    root: portalRoot,
    base: isGithubPages ? '/VES/' : '/',
    build: {
      outDir: resolve(currentDir, 'dist'),
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
  };
});
