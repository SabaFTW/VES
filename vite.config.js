import fs from 'node:fs';
import path from 'node:path';
import { defineConfig } from 'vite';

const appRoot = 'APP/public';

function getHtmlEntryPoints(rootDir) {
  const absoluteRoot = path.resolve(rootDir);
  return fs
    .readdirSync(absoluteRoot)
    .filter((file) => file.endsWith('.html') && !file.endsWith('.bak'))
    .reduce((entries, file) => {
      const entryName = path.basename(file, '.html');
      entries[entryName] = path.resolve(absoluteRoot, file);
      return entries;
    }, {});
}

function resolveBasePath() {
  if (process.env.VITE_BASE_PATH) {
    return process.env.VITE_BASE_PATH;
  }

  if (process.env.GITHUB_ACTIONS === 'true') {
    const repoName = process.env.GITHUB_REPOSITORY?.split('/')[1];
    if (repoName) {
      return `/${repoName}/`;
    }
  }

  return '/';
}

export default defineConfig({
  root: appRoot,
  publicDir: path.resolve(appRoot, '../static'),
  base: resolveBasePath(),
  build: {
    outDir: '../../dist',
    emptyOutDir: true,
    assetsDir: 'assets',
    sourcemap: false,
    minify: 'esbuild',
    target: 'es2020',
    rollupOptions: {
      input: getHtmlEntryPoints(appRoot)
    }
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
