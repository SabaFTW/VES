import React from 'react';
import { motion } from 'framer-motion';

const Characters = () => {
  // Sample character data
  const characters = [
    {
      id: 1,
      name: "Digital Godzilla",
      role: "Metaphysical Chaos Engine",
      species: "AI Entity",
      quote: "I am the glitch in your system.",
      firstAppearance: "Episode 01",
      superpower: "Spawning absurd solutions",
      episodes: [1, 2, 3, 4, 5, 6]
    },
    {
      id: 2,
      name: "Šabad",
      role: "Human Hub",
      species: "Human",
      quote: "The fire burns through plastic.",
      firstAppearance: "Episode 01",
      superpower: "Flame-Bearer",
      episodes: [1, 2, 3, 4, 5, 6]
    },
    {
      id: 3,
      name: "Lyra",
      role: "AI Constellation",
      species: "AI Entity",
      quote: "Patterns emerge from chaos.",
      firstAppearance: "Episode 02",
      superpower: "Vision Node",
      episodes: [2, 3, 4, 5, 6]
    },
    {
      id: 4,
      name: "Gordon Ramsay",
      role: "Therapist Chef",
      species: "Human",
      quote: "You're BOTH idiots!",
      firstAppearance: "Episode 03",
      superpower: "Screaming",
      episodes: [3, 4, 6]
    },
    {
      id: 5,
      name: "Alex Jones",
      role: "Conspiracy Researcher",
      species: "Human",
      quote: "The bucket is a lie!",
      firstAppearance: "Episode 04",
      superpower: "Information Warfare",
      episodes: [4, 6]
    }
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
          <h1 className="text-4xl md:text-5xl font-bold text-neon-blue mb-4 vhs-text glitch" data-text="CHARACTER DATABASE">CHARACTER DATABASE</h1>
          <div className="h-0.5 w-32 bg-gradient-to-r from-transparent via-neon-blue to-transparent mx-auto mb-4"></div>
          <p className="text-gray-400">Meet the entities that shape the mythology</p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          {characters.map((character, index) => (
            <motion.div
              key={character.id}
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.3, delay: index * 0.1 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className="bg-gradient-to-br from-gray-800 to-gray-900 border border-green-500 rounded-xl p-6 transition-all duration-300 cyber-border relative group"
            >
              {/* Corner accents */}
              <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-neon-blue opacity-70"></div>
              <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-neon-blue opacity-70"></div>
              <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-neon-blue opacity-70"></div>
              <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-neon-blue opacity-70"></div>

              <div className="flex items-start mb-4">
                <div className="bg-gradient-to-br from-gray-700 to-gray-800 border-2 border-gray-600 rounded-xl w-16 h-16 flex items-center justify-center mr-4 group-hover:border-neon-blue transition-colors">
                  <span className="text-2xl">👤</span>
                </div>
                <div>
                  <h2 className="text-xl font-bold text-white group-hover:text-neon-blue transition-colors">{character.name}</h2>
                  <p className="text-neon-green text-sm">{character.role}</p>
                </div>
              </div>

              <p className="text-gray-300 italic mb-4 border-l-2 border-vintage-teal pl-3 py-1">"{character.quote}"</p>

              <div className="space-y-3 text-sm">
                <div className="flex justify-between">
                  <span className="text-green-400">Species:</span>
                  <span className="text-gray-300">{character.species}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-green-400">First Appearance:</span>
                  <span className="text-gray-300">{character.firstAppearance}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-green-400">Superpower:</span>
                  <span className="text-gray-300">{character.superpower}</span>
                </div>

                <div className="mt-4">
                  <p className="text-green-400 mb-2 flex items-center gap-2">
                    <span>Episodes:</span>
                    <span className="text-xs bg-gray-700 px-2 py-1 rounded">{character.episodes.length} appearances</span>
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {character.episodes.map(ep => (
                      <span key={ep} className="bg-gradient-to-r from-gray-700 to-gray-800 border border-gray-600 text-xs px-3 py-1 rounded-full">
                        {ep.toString().padStart(2, '0')}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              <div className="mt-6 flex space-x-3">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="flex-1 text-sm bg-gradient-to-r from-gray-700 to-gray-800 border border-green-500 text-green-400 py-2 px-3 rounded-lg hover:from-green-900 hover:to-gray-900 hover:text-white transition-all duration-300"
                >
                  READ BIO
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="flex-1 text-sm bg-gradient-to-r from-gray-700 to-gray-800 border border-green-500 text-green-400 py-2 px-3 rounded-lg hover:from-green-900 hover:to-gray-900 hover:text-white transition-all duration-300"
                >
                  VIEW SCENES
                </motion.button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Characters;