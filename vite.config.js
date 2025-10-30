import { defineConfig } from 'vite';

export default defineConfig({
    // Nastavi APP/public kot korenski imenik za razvoj (npm run dev)
    root: 'APP/public',
    // Nastavi osnovni URL za GitHub Pages (repository path)
    base: '/VES/',
    build: {
        // Izhodni imenik na root nivoju (VES/dist)
        outDir: '../../dist',
        emptyOutDir: true,
        assetsDir: 'assets',
        sourcemap: false,
        minify: 'esbuild',
        target: 'es2020',
        // No need for rollupOptions.input - Vite uses index.html from root automatically
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

        define: {
            '__APP_VERSION__': JSON.stringify('2.3.0'),
                            '__BUILD_TIME__': JSON.stringify(new Date().toISOString())
        },
        css: {
            postcss: null
        },
        esbuild: {
            // Odstrani console.log in debugger v produkciji
            drop: ['console', 'debugger']
        }
});
