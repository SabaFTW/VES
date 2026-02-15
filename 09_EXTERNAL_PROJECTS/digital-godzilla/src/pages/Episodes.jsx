import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';

const Episodes = () => {
  // Sample episode data
  const episodes = [
    { id: 1, title: "The Spawning", duration: "15 min read", thumbnail: "/images/ep01-thumbnail.jpg" },
    { id: 2, title: "The Bucket Protocol", duration: "18 min read", thumbnail: "/images/ep02-thumbnail.jpg" },
    { id: 3, title: "Gordon's Kitchen", duration: "20 min read", thumbnail: "/images/ep03-thumbnail.jpg" },
    { id: 4, title: "The Tractor Paradox", duration: "17 min read", thumbnail: "/images/ep04-thumbnail.jpg" },
    { id: 5, title: "Oracle's Truth", duration: "22 min read", thumbnail: "/images/ep05-thumbnail.jpg" },
    { id: 6, title: "The Oracle That Couldn't Lie", duration: "18 min read", thumbnail: "/images/ep06-thumbnail.jpg" },
  ];

  return (
    <div className="py-8 relative">
      {/* Background elements */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-0 left-0 w-full h-full grid-pattern opacity-10"></div>
      </div>

      <div className="relative z-10">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-neon-blue mb-4 vhs-text glitch" data-text="EPISODES">EPISODES</h1>
          <div className="h-0.5 w-24 bg-gradient-to-r from-transparent via-neon-blue to-transparent mx-auto"></div>
          <p className="text-gray-400 mt-4">Navigate the mythology. Choose your chaos.</p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {episodes.map((episode, index) => (
            <motion.div
              key={episode.id}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: index * 0.1 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className="bg-gradient-to-br from-gray-800 to-gray-900 border border-green-500 rounded-lg overflow-hidden transition-all duration-300 cyber-border relative group"
            >
              <div className="p-6">
                <div className="flex justify-between items-start mb-4">
                  <div className="bg-gray-900 text-neon-blue px-3 py-1 rounded text-sm font-mono">
                    EP {episode.id.toString().padStart(2, '0')}
                  </div>
                  <div className="bg-gray-900 text-gray-400 px-2 py-1 rounded text-xs">
                    {episode.duration}
                  </div>
                </div>

                <h3 className="text-xl font-bold text-white mb-3 group-hover:text-neon-blue transition-colors">{episode.title}</h3>

                <div className="mt-6">
                  <Link
                    to={`/episode/${episode.id}`}
                    className="inline-flex items-center gap-2 bg-gradient-to-r from-gray-800 to-gray-900 border border-green-500 text-green-400 py-2 px-4 rounded-lg hover:from-green-900 hover:to-gray-900 hover:text-white transition-all duration-300 shadow-lg shadow-green-500/10 hover:shadow-green-500/30"
                  >
                    <span>▶</span> WATCH
                  </Link>
                </div>
              </div>

              {/* Animated corner accents */}
              <div className="absolute top-0 left-0 w-6 h-6 border-t-2 border-l-2 border-neon-blue opacity-70"></div>
              <div className="absolute top-0 right-0 w-6 h-6 border-t-2 border-r-2 border-neon-blue opacity-70"></div>
              <div className="absolute bottom-0 left-0 w-6 h-6 border-b-2 border-l-2 border-neon-blue opacity-70"></div>
              <div className="absolute bottom-0 right-0 w-6 h-6 border-b-2 border-r-2 border-neon-blue opacity-70"></div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Episodes;