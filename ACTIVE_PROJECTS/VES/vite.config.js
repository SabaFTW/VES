import { defineConfig } from 'vite';

export default defineConfig({
    root: 'APP/public',
    base: './',
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
        cors: true,
    },
    preview: {
        port: 4173,
        host: true,
        cors: true
    },
    publicDir: false,
    define: {
        '__APP_VERSION__': JSON.stringify(process.env.npm_package_version || '2.3.0'),
        '__BUILD_TIME__': JSON.stringify(new Date().toISOString())
    },
    css: {
        postcss: null
    },
    esbuild: {
        drop: ['console', 'debugger']
    }
});
