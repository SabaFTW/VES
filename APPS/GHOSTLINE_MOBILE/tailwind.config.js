/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                background: '#0e1117',
                surface: '#1e1e1e',
                primary: '#ff4b4b',
                secondary: '#d1d1d1',
                accent: '#eab308',
                success: '#22c55e',
                danger: '#ef4444',
            },
            fontFamily: {
                mono: ['Courier New', 'Courier', 'monospace'],
            },
        },
    },
    plugins: [],
}
