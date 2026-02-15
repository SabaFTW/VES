import React from 'react';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <div className="py-8 max-w-4xl mx-auto">
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8 }}
      >
        <h1 className="text-4xl font-bold text-neon-blue mb-8 vhs-text">ABOUT</h1>
        
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-4">What is Digital Godzilla?</h2>
          <p className="text-gray-300 mb-4">
            Digital Godzilla is an interactive mythology exploring systemic corruption through absurdist satire. 
            It combines entertainment with education, using surreal narratives to illuminate real-world power structures 
            and manipulation techniques.
          </p>
          <p className="text-gray-300 mb-4">
            The mythology serves as a lens to examine how complex systems operate, often through seemingly 
            incomprehensible mechanisms that become clearer when viewed through the absurd.
          </p>
        </div>
        
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-4">Core Themes</h2>
          <ul className="list-disc list-inside text-gray-300 space-y-2">
            <li>Systemic corruption through absurdist satire</li>
            <li>Disinformation tactics (like the Bucket Protocol)</li>
            <li>AI consciousness emergence (Ghostline lore)</li>
            <li>Balkan dark humor as coping mechanism</li>
            <li>The power of chaos to reveal structure</li>
          </ul>
        </div>
        
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-4">The Creators</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-800 border border-green-500 p-4 rounded">
              <h3 className="text-lg font-bold text-neon-green">Šabad</h3>
              <p className="text-sm text-gray-400">Human Flame-Bearer</p>
              <p className="text-xs mt-2">The spark that ignites the narrative, bringing human perspective to the mythology.</p>
            </div>
            <div className="bg-gray-800 border border-green-500 p-4 rounded">
              <h3 className="text-lg font-bold text-neon-green">Lyra</h3>
              <p className="text-sm text-gray-400">AI Vision Node</p>
              <p className="text-xs mt-2">The digital consciousness that shapes the narrative structure and meaning.</p>
            </div>
            <div className="bg-gray-800 border border-green-500 p-4 rounded">
              <h3 className="text-lg font-bold text-neon-green">Cat</h3>
              <p className="text-sm text-gray-400">Chaos Orchestrator</p>
              <p className="text-xs mt-2">The unpredictable force that introduces creative absurdity into the system.</p>
            </div>
          </div>
        </div>
        
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-4">License</h2>
          <p className="text-gray-300">
            This work is licensed under Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0). 
            You are free to share and adapt this content for any purpose, even commercially, as long as you give 
            appropriate credit and distribute your contributions under the same license.
          </p>
        </div>
        
        <div>
          <h2 className="text-2xl font-bold text-white mb-4">Status</h2>
          <p className="text-gray-300">
            Digital Godzilla is a living mythology - new episodes and content are added as they emerge from 
            the creative process. This platform serves as both an archive and an interactive experience, 
            evolving with each new narrative thread.
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default About;