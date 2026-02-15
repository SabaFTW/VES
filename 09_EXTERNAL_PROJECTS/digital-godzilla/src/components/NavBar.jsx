import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = () => {
  return (
    <nav className="bg-gray-800 border-b border-green-500 py-4 scan-lines">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-neon-blue vhs-text">
          <span className="glitch" data-text="DIGITAL GODZILLA">DIGITAL GODZILLA</span>
        </Link>
        <div className="flex space-x-6">
          <Link to="/" className="text-green-400 hover:text-neon-blue transition-colors">HOME</Link>
          <Link to="/episodes" className="text-green-400 hover:text-neon-blue transition-colors">EPISODES</Link>
          <Link to="/characters" className="text-green-400 hover:text-neon-blue transition-colors">CHARACTERS</Link>
          <Link to="/codex" className="text-green-400 hover:text-neon-blue transition-colors">CODEX</Link>
          <Link to="/about" className="text-green-400 hover:text-neon-blue transition-colors">ABOUT</Link>
        </div>
      </div>
    </nav>
  );
};

export default NavBar;