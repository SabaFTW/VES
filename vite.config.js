import { defineConfig } from 'vite';

export default defineConfig({
    // Nastavi APP/public kot korenski imenik za razvoj (npm run dev)
    root: 'APP/public',
    // Nastavi osnovni URL za GitHub Pages (relativne poti)
    base: './',
    build: {
        // Izhodni imenik na root nivoju (VES/dist)
        outDir: '../dist',
        emptyOutDir: true,
        assetsDir: 'assets',
        sourcemap: false,
        minify: 'esbuild',
        target: 'es2020',
        rollupOptions: {
            input: {
                main: 'APP/public/index.html'
            }
        }
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
    // Povezava public direktorija v APP/public
    publicDir: 'APP/public',
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
