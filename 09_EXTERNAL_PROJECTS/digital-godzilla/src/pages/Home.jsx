import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center text-center relative overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-0 left-0 w-full h-full grid-pattern opacity-20"></div>
        <div className="absolute top-0 left-0 w-full h-full digital-rain"></div>

        {/* Particle Field */}
        <div className="particle-field">
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
          <div className="particle"></div>
        </div>

        {/* Sacred Geometry Overlay */}
        <div className="sacred-geometry-bg"></div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="mb-12 relative z-10 cyber-border p-1 rounded-lg bg-gray-900"
      >
        <h1 className="text-5xl md:text-7xl font-bold text-neon-blue mb-2 vhs-text glitch" data-text="DIGITAL GODZILLA">
          DIGITAL GODZILLA
        </h1>
        <div className="h-1 w-32 bg-gradient-to-r from-transparent via-neon-blue to-transparent mx-auto mb-4"></div>
        <p className="text-xl text-green-400 mb-6">THE INTERACTIVE MYTHOLOGY</p>
        <p className="text-base md:text-lg text-gray-300 max-w-2xl mx-auto mb-10">
          10 Episodes. Infinite Chaos. Watch the Absurd Reveal the Structure.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 max-w-md mx-auto">
          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Link
              to="/episodes"
              className="block bg-gradient-to-r from-gray-800 to-gray-900 border border-green-500 text-green-400 py-3 px-6 rounded-lg hover:from-green-900 hover:to-gray-900 hover:text-white transition-all duration-300 shadow-lg shadow-green-500/20 hover:shadow-green-500/40"
            >
              START WATCHING
            </Link>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            <Link
              to="/codex"
              className="block bg-gradient-to-r from-gray-800 to-gray-900 border border-green-500 text-green-400 py-3 px-6 rounded-lg hover:from-green-900 hover:to-gray-900 hover:text-white transition-all duration-300 shadow-lg shadow-green-500/20 hover:shadow-green-500/40"
            >
              EXPLORE CODEX
            </Link>
          </motion.div>
        </div>
      </motion.div>

      {/* Animated digital rain background effect */}
      <div className="fixed inset-0 overflow-hidden -z-10 pointer-events-none">
        {Array.from({ length: 100 }).map((_, i) => (
          <motion.div
            key={i}
            className="absolute text-green-900 opacity-10 font-mono"
            style={{
              left: `${Math.random() * 100}%`,
              fontSize: `${Math.random() * 10 + 8}px`,
            }}
            initial={{ y: -20, opacity: 0 }}
            animate={{
              y: window.innerHeight + 20,
              opacity: [0, 0.1, 0],
            }}
            transition={{
              duration: Math.random() * 5 + 3,
              repeat: Infinity,
              delay: Math.random() * 4,
            }}
          >
            {String.fromCharCode(Math.random() * 94 + 33)} {/* Random ASCII chars */}
          </motion.div>
        ))}
      </div>

      {/* Floating particles */}
      {Array.from({ length: 20 }).map((_, i) => (
        <motion.div
          key={`particle-${i}`}
          className="absolute rounded-full bg-neon-blue opacity-20"
          style={{
            width: `${Math.random() * 10 + 2}px`,
            height: `${Math.random() * 10 + 2}px`,
            top: `${Math.random() * 100}%`,
            left: `${Math.random() * 100}%`,
          }}
          animate={{
            y: [0, -20, 0],
            x: [0, Math.random() * 40 - 20, 0],
            opacity: [0.1, 0.4, 0.1],
          }}
          transition={{
            duration: Math.random() * 4 + 2,
            repeat: Infinity,
            ease: "easeInOut"
          }}
        />
      ))}
    </div>
  );
};

export default Home;