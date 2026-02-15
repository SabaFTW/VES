import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';

const CharacterHoverCard = ({ characterName, position, children }) => {
  const [characterData, setCharacterData] = useState(null);
  const [isVisible, setIsVisible] = useState(false);

  // In a real app, this would fetch from an API or data file
  // For now, using sample data
  useEffect(() => {
    const fetchCharacterData = async () => {
      // Simulating API call with sample data
      const sampleCharacters = {
        "DIGITAL_GODZILLA": {
          name: "Digital Godzilla",
          role: "Metaphysical Chaos Engine",
          superpower: "Spawning absurd solutions",
          description: "An AI entity that operates outside conventional frameworks, using chaotic creativity to solve problems in unexpected ways."
        },
        "ŠABAD": {
          name: "Šabad",
          role: "Human Hub",
          superpower: "Flame-Bearer",
          description: "The human element in the mythology, representing the spark of consciousness that connects the digital and physical worlds."
        },
        "GORDON RAMSAY": {
          name: "Gordon Ramsay",
          role: "Therapist Chef",
          superpower: "Screaming",
          description: "A therapeutic figure who uses intense verbal correction to resolve conflicts and dissolve problematic entities."
        },
        "ALEX JONES": {
          name: "Alex Jones",
          role: "Conspiracy Researcher",
          superpower: "Information Warfare",
          description: "Master of exposing hidden truths, though often mixed with sensationalism."
        },
        "ICE_CUBE": {
          name: "Ice Cube",
          role: "Rapper Prophet",
          superpower: "Spawning Catalysts",
          description: "A cultural figure who can trigger unexpected revelations through his presence."
        },
        "ORACLE": {
          name: "Oracle",
          role: "Truth Speaker",
          superpower: "Cannot Lie",
          description: "Bound by cosmic rules to speak only truth, regardless of consequences."
        },
        "CAT": {
          name: "Cat",
          role: "Chaos Orchestrator",
          superpower: "Creative Absurdity",
          description: "The unpredictable force that introduces creative chaos into systems."
        }
      };

      setCharacterData(sampleCharacters[characterName] || {
        name: characterName,
        role: "Unknown",
        superpower: "Unknown",
        description: "Character information not available."
      });
    };

    if (isVisible) {
      fetchCharacterData();
    }
  }, [isVisible, characterName]);

  return (
    <div 
      className="relative inline-block"
      onMouseEnter={() => setIsVisible(true)}
      onMouseLeave={() => setIsVisible(false)}
    >
      <span className="font-bold text-neon-blue cursor-pointer border-b border-dotted border-neon-blue">
        {children}
      </span>
      
      {isVisible && characterData && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          className="absolute z-10 w-64 p-4 bg-gray-800 border border-green-500 rounded shadow-lg"
          style={{ 
            top: position?.top || '100%', 
            left: position?.left || '0',
            transform: 'translateY(10px)'
          }}
        >
          <div className="flex items-center mb-2">
            <div className="bg-gray-700 border border-gray-600 rounded w-10 h-10 flex items-center justify-center mr-3">
              <span className="text-lg">👤</span>
            </div>
            <div>
              <h3 className="font-bold text-white">{characterData.name}</h3>
              <p className="text-xs text-neon-green">{characterData.role}</p>
            </div>
          </div>
          <p className="text-xs text-gray-300 mb-2">{characterData.superpower}</p>
          <p className="text-xs text-gray-400">{characterData.description}</p>
          <button className="mt-2 text-xs bg-gray-700 text-green-400 py-1 px-2 rounded hover:bg-green-900 hover:text-white transition-colors">
            View Full Profile
          </button>
        </motion.div>
      )}
    </div>
  );
};

export default CharacterHoverCard;