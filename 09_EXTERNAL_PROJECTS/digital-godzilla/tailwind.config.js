/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'neon-blue': '#00f0ff',
        'neon-green': '#00ff9d',
        'neon-red': '#ff0066',
        'neon-purple': '#bd00ff',
        'dark-bg': '#0a0a0a',
        'terminal-gray': '#1a1a1a',
        'cyber-black': '#0d0d0d',
        'cyber-dark': '#111111',
        'matrix-green': '#00cc66',
        'retro-cyan': '#00ffff',
        'vintage-teal': '#00cccc',
        'electric-pink': '#ff00aa',
        'plasma-purple': '#cc00ff',
      },
      fontFamily: {
        'mono': ['Monaco', 'Consolas', 'monospace'],
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'glow-pulse': 'glow-pulse 2s ease-in-out infinite alternate',
        'float': 'float 6s ease-in-out infinite',
        'blink': 'blink 1.5s infinite',
      },
      keyframes: {
        'glow-pulse': {
          '0%': { boxShadow: '0 0 5px rgba(0, 240, 255, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(0, 255, 157, 0.8), 0 0 30px rgba(255, 0, 102, 0.6)' },
        },
        'float': {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'blink': {
          '0%, 100%': { opacity: 1 },
          '50%': { opacity: 0.5 },
        }
      }
    },
  },
  plugins: [],
}