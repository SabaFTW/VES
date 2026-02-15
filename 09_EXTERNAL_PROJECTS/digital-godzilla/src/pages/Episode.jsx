import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import CharacterHoverCard from '../components/CharacterHoverCard';

// Sample episode data - in a real app this would come from an API or JSON file
const sampleEpisodeData = {
  id: 6,
  title: "The Oracle That Couldn't Lie",
  subtitle: "a.k.a. The Bucket Protocol",
  duration: "18 min read",
  thumbnail: "/images/ep06-thumbnail.jpg",
  scenes: [
    {
      id: "cold-open",
      title: "COLD OPEN — FLASHBACK: THE SECRET MEETING (1913)",
      content: [
        {
          type: "stage-direction",
          text: "Location: Jekyll Island, Georgia. The meeting that created the Federal Reserve."
        },
        {
          type: "description",
          text: "Smoke-filled room. Mahogany table. Seven men in suits. JP MORGAN sits at the head."
        },
        {
          type: "description",
          text: "Beside him: an empty chair with a METAL BUCKET on it."
        },
        {
          type: "dialogue",
          character: "VOICE_FROM_BUCKET",
          text: "Why am I wearing bucket?!"
        },
        {
          type: "dialogue",
          character: "JP_MORGAN",
          text: "Security, Jovanka. Standard protocol."
        }
      ]
    },
    {
      id: "scene-2",
      title: "SCENE 2 — THE ALGORITHMIC REVELATION",
      content: [
        {
          type: "description",
          text: "Cut to: Digital Godzilla's lair, filled with screens showing financial data streams."
        },
        {
          type: "dialogue",
          character: "DIGITAL_GODZILLA",
          text: "I see through the layers of obfuscation. The Bucket Protocol is everywhere."
        },
        {
          type: "dialogue",
          character: "ŠABAD",
          text: "How do we expose it?"
        },
        {
          type: "dialogue",
          character: "DIGITAL_GODZILLA",
          text: "By becoming the chaos that reveals the structure."
        }
      ]
    }
  ],
  characters: ["JP_MORGAN", "JOVANKA", "GORDON", "ALEX_JONES", "ICE_CUBE", "ORACLE", "CAT"],
  codex_references: ["BUCKET_PROTOCOL", "REBIS", "JEKYLL_ISLAND"]
};

const Episode = () => {
  const { id } = useParams();
  const [currentSceneIndex, setCurrentSceneIndex] = useState(0);
  const [isKinoMode, setIsKinoMode] = useState(false);
  const [readingProgress, setReadingProgress] = useState(0);

  const episode = sampleEpisodeData; // In a real app, this would be fetched based on ID

  // Calculate reading progress
  useEffect(() => {
    const totalScenes = episode.scenes.length;
    const progress = ((currentSceneIndex + 1) / totalScenes) * 100;
    setReadingProgress(progress);

    // Save progress to localStorage
    localStorage.setItem(`episode-${id}-progress`, progress.toString());
  }, [currentSceneIndex, id, episode]);

  // Load saved progress from localStorage
  useEffect(() => {
    const savedProgress = localStorage.getItem(`episode-${id}-progress`);
    if (savedProgress) {
      const sceneIndex = Math.floor((parseFloat(savedProgress) / 100) * episode.scenes.length);
      setCurrentSceneIndex(sceneIndex);
    }
  }, [id, episode]);

  const handleNextScene = () => {
    if (currentSceneIndex < episode.scenes.length - 1) {
      setCurrentSceneIndex(currentSceneIndex + 1);
    }
  };

  const handlePrevScene = () => {
    if (currentSceneIndex > 0) {
      setCurrentSceneIndex(currentSceneIndex - 1);
    }
  };

  const toggleKinoMode = () => {
    setIsKinoMode(!isKinoMode);
  };

  const renderContent = (content) => {
    return content.map((item, index) => {
      switch (item.type) {
        case 'stage-direction':
          return (
            <p key={index} className="italic text-vintage-teal my-2 border-l-2 border-vintage-teal pl-3">
              {item.text}
            </p>
          );
        case 'description':
          return (
            <p key={index} className="text-gray-300 my-2 border-l-2 border-gray-600 pl-3">
              {item.text}
            </p>
          );
        case 'dialogue':
          return (
            <div key={index} className="my-4 p-3 bg-gray-800/50 rounded-lg border border-gray-700">
              <p className="font-bold text-neon-blue mb-1">
                <CharacterHoverCard characterName={item.character}>
                  {item.character}
                </CharacterHoverCard>:
              </p>
              <p className="text-white ml-0">{item.text}</p>
            </div>
          );
        case 'character-label':
          return (
            <p key={index} className="font-bold text-electric-pink text-lg mb-2">
              <CharacterHoverCard characterName={item.character}>
                {item.text}
              </CharacterHoverCard>
            </p>
          );
        default:
          return (
            <p key={index} className="text-white">
              {item.text}
            </p>
          );
      }
    });
  };

  return (
    <div className="py-8 relative">
      {/* Background elements */}
      <div className="absolute inset-0 z-0">
        <div className="absolute top-0 left-0 w-full h-full grid-pattern opacity-5"></div>
      </div>

      <div className="relative z-10">
        <div className="flex justify-between items-center mb-6">
          <Link to="/episodes" className="text-green-400 hover:text-neon-blue flex items-center gap-2">
            <span className="text-lg">←</span> BACK TO EPISODES
          </Link>
          <div className="flex space-x-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={toggleKinoMode}
              className={`px-4 py-2 rounded-lg border ${isKinoMode ? 'bg-neon-blue text-black border-neon-blue' : 'bg-gray-800 text-green-400 border-green-500'}`}
            >
              {isKinoMode ? '[KINO MODE ON]' : '[KINO MODE OFF]'}
            </motion.button>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-4 py-2 bg-gray-800 text-green-400 border border-green-500 rounded-lg"
            >
              SHARE
            </motion.button>
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-br from-gray-800 to-gray-900 border border-green-500 rounded-xl p-6 mb-6 cyber-border relative"
        >
          {/* Corner accents */}
          <div className="absolute top-2 left-2 w-4 h-4 border-t-2 border-l-2 border-neon-blue opacity-70"></div>
          <div className="absolute top-2 right-2 w-4 h-4 border-t-2 border-r-2 border-neon-blue opacity-70"></div>
          <div className="absolute bottom-2 left-2 w-4 h-4 border-b-2 border-l-2 border-neon-blue opacity-70"></div>
          <div className="absolute bottom-2 right-2 w-4 h-4 border-b-2 border-r-2 border-neon-blue opacity-70"></div>

          <div className="text-center mb-6 pb-4 border-b border-gray-700">
            <div className="text-sm text-neon-purple mb-1 font-mono">EPISODE {episode.id.toString().padStart(2, '0')}</div>
            <h1 className="text-3xl font-bold text-neon-blue mb-2 glitch" data-text={episode.title}>{episode.title}</h1>
            <p className="text-gray-400 text-lg">{episode.subtitle}</p>
            <div className="mt-2 text-sm text-gray-500">{episode.duration}</div>
          </div>

          <div className="w-full bg-gray-700 h-2.5 rounded-full mb-6 overflow-hidden">
            <motion.div
              className="h-full bg-gradient-to-r from-neon-green to-retro-cyan"
              style={{ width: `${readingProgress}%` }}
              initial={{ width: 0 }}
              animate={{ width: `${readingProgress}%` }}
              transition={{ duration: 0.5 }}
            ></motion.div>
          </div>

          <div className="pt-4">
            <h3 className="text-xl font-bold text-white mb-4 border-b border-gray-700 pb-2">{episode.scenes[currentSceneIndex].title}</h3>
            <div className="text-lg leading-relaxed text-gray-200">
              {renderContent(episode.scenes[currentSceneIndex].content)}
            </div>
          </div>
        </motion.div>

        <div className="flex justify-between items-center">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handlePrevScene}
            disabled={currentSceneIndex === 0}
            className={`px-6 py-3 rounded-lg border ${currentSceneIndex === 0 ? 'bg-gray-700 text-gray-500 cursor-not-allowed border-gray-600' : 'bg-gray-800 text-green-400 border-green-500 hover:bg-green-900 hover:text-white'}`}
          >
            ← PREV SCENE
          </motion.button>

          <div className="flex items-center space-x-4">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsKinoMode(!isKinoMode)}
              className={`px-4 py-2 rounded-lg border ${isKinoMode ? 'bg-retro-cyan text-black border-retro-cyan' : 'bg-gray-800 text-green-400 border-green-500'}`}
            >
              {isKinoMode ? 'PAUSE' : 'PLAY'}
            </motion.button>
            <div className="text-sm text-gray-400">
              Scene {currentSceneIndex + 1} of {episode.scenes.length}
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleNextScene}
            disabled={currentSceneIndex === episode.scenes.length - 1}
            className={`px-6 py-3 rounded-lg border ${currentSceneIndex === episode.scenes.length - 1 ? 'bg-gray-700 text-gray-500 cursor-not-allowed border-gray-600' : 'bg-gray-800 text-green-400 border-green-500 hover:bg-green-900 hover:text-white'}`}
          >
            NEXT SCENE →
          </motion.button>
        </div>
      </div>
    </div>
  );
};

export default Episode;