import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Episodes from './pages/Episodes';
import Episode from './pages/Episode';
import Characters from './pages/Characters';
import Codex from './pages/Codex';
import About from './pages/About';
import NavBar from './components/NavBar';
import Footer from './components/Footer';

function App() {
  return (
    <>
      {/* Global Enhanced Styles - Inline for guaranteed load */}
      <style>{`
        /* Sacred Geometry Background */
        @keyframes sacred-pulse {
          0%, 100% { opacity: 0.03; transform: scale(1) rotate(0deg); }
          50% { opacity: 0.08; transform: scale(1.05) rotate(180deg); }
        }
        @keyframes metatron-spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .sacred-geometry-bg {
          position: fixed; top: 0; left: 0; width: 100%; height: 100%;
          pointer-events: none; z-index: 0; overflow: hidden;
        }
        .sacred-geometry-bg::before {
          content: ''; position: absolute; top: 50%; left: 50%;
          width: 800px; height: 800px; margin: -400px 0 0 -400px;
          background:
            radial-gradient(circle, transparent 30%, rgba(217, 119, 6, 0.05) 31%, transparent 32%),
            radial-gradient(circle, transparent 45%, rgba(217, 119, 6, 0.05) 46%, transparent 47%),
            radial-gradient(circle, transparent 60%, rgba(217, 119, 6, 0.05) 61%, transparent 62%);
          animation: sacred-pulse 8s ease-in-out infinite, metatron-spin 120s linear infinite;
        }

        /* 432Hz Glow Effect */
        @keyframes hz-432-pulse {
          0%, 100% { box-shadow: 0 0 10px rgba(217, 119, 6, 0.3), 0 0 20px rgba(217, 119, 6, 0.2); }
          50% { box-shadow: 0 0 20px rgba(217, 119, 6, 0.6), 0 0 40px rgba(217, 119, 6, 0.4), 0 0 60px rgba(217, 119, 6, 0.2); }
        }
        .hz-432-glow {
          animation: hz-432-pulse 2.31s ease-in-out infinite;
        }

        /* Particle Effects */
        @keyframes particle-float {
          0%, 100% { transform: translateY(0) translateX(0); opacity: 0.3; }
          50% { transform: translateY(-20px) translateX(10px); opacity: 0.8; }
        }
        .particle-field {
          position: absolute; top: 0; left: 0; width: 100%; height: 100%;
          overflow: hidden; pointer-events: none;
        }
        .particle {
          position: absolute; width: 2px; height: 2px;
          background: radial-gradient(circle, rgba(217, 119, 6, 1) 0%, transparent 70%);
          border-radius: 50%;
          animation: particle-float 8s ease-in-out infinite;
        }
        .particle:nth-child(1) { left: 10%; top: 20%; animation-delay: 0s; }
        .particle:nth-child(2) { left: 25%; top: 40%; animation-delay: 1s; width: 3px; height: 3px; }
        .particle:nth-child(3) { left: 40%; top: 60%; animation-delay: 2s; }
        .particle:nth-child(4) { left: 60%; top: 30%; animation-delay: 1.5s; width: 4px; height: 4px; }
        .particle:nth-child(5) { left: 75%; top: 70%; animation-delay: 0.5s; }
        .particle:nth-child(6) { left: 85%; top: 50%; animation-delay: 2.5s; }
        .particle:nth-child(7) { left: 15%; top: 80%; animation-delay: 1.2s; }
        .particle:nth-child(8) { left: 50%; top: 15%; animation-delay: 3s; width: 3px; height: 3px; }

        /* Enhanced Card Styles */
        .codex-card {
          border-left: 4px solid rgba(217, 119, 6, 0.3);
          transition: all 0.5s cubic-bezier(0.16, 1, 0.3, 1);
        }
        .codex-card:hover {
          border-left-color: rgba(217, 119, 6, 1);
          transform: translateX(8px);
          box-shadow: -8px 0 24px rgba(217, 119, 6, 0.2);
        }

        /* Scroll Reveal */
        @keyframes reveal-from-bottom {
          from { opacity: 0; transform: translateY(60px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .scroll-reveal {
          animation: reveal-from-bottom 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards;
        }
        .scroll-reveal-delay-1 { animation-delay: 0.1s; }
        .scroll-reveal-delay-2 { animation-delay: 0.2s; }
        .scroll-reveal-delay-3 { animation-delay: 0.3s; }
        .scroll-reveal-delay-4 { animation-delay: 0.4s; }
      `}</style>

      <div className="min-h-screen bg-gray-900 text-green-400 font-mono relative">
        {/* Sacred Geometry Background Layer */}
        <div className="sacred-geometry-bg"></div>

        <NavBar />
        <main className="container mx-auto px-4 py-8 relative z-10">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/episodes" element={<Episodes />} />
            <Route path="/episode/:id" element={<Episode />} />
            <Route path="/characters" element={<Characters />} />
            <Route path="/codex" element={<Codex />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </>
  );
}

export default App;