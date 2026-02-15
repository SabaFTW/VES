import React, { useState, useEffect } from 'react';
import Header from './components/Header';


// Section Components (to be created based on the provided HTML)
import BiasSection from './sections/BiasSection';
import ConsciousnessSection from './sections/ConsciousnessSection';
import SheepWolfSection from './sections/SheepWolfSection';
import AnalysisSection from './sections/AnalysisSection';
import PlannerSection from './sections/PlannerSection';
import LandingSection from './sections/LandingSection';
import FileBrowserSection from './components/FileBrowserSection'; // New section for file navigation

// Combined CSS from the provided HTML
const customCss = `
    body { font-family: 'Inter', sans-serif; }
    .task-item:hover .delete-btn, .task-item:hover .breakdown-btn { opacity: 1; }
    .delete-btn, .breakdown-btn { opacity: 0; transition: opacity 0.2s ease-in-out; }
    .completed { text-decoration: line-through; color: #6b7280; }
    .loader { border: 2px solid #f3f3f3; border-top: 2px solid #3498db; border-radius: 50%; width: 16px; height: 16px; animation: spin 1s linear infinite; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .bias-btn, .path-choice { transition: all 0.3s ease; }
    .bias-btn:hover, .path-choice:hover { transform: translateY(-5px); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2); }
    .path { stroke-dasharray: 1000; stroke-dashoffset: 1000; }
    .path.animate { animation: draw 3s ease-in-out forwards; }
    @keyframes draw { to { stroke-dashoffset: 0; } }
    .fade-in { opacity: 0; transition: opacity 0.5s ease-in-out; }
    .fade-in.visible { opacity: 1; }
    .accent-color { color: #008080; }
    .dark .accent-color { color: #2dd4bf; }
    .bg-accent-color { background-color: #008080; }
    .dark .bg-accent-color { background-color: #14b8a6; }
    .border-accent-color { border-color: #008080; }
    .dark .border-accent-color { border-color: #14b8a6; }
    .section-hidden { display: none; }
    .flame-pulse { animation: flame-pulse 2s ease-in-out infinite; }
    @keyframes flame-pulse { 0%, 100% { opacity: 0.8; transform: scale(1); } 50% { opacity: 1; transform: scale(1.05); } }
    .weave-pattern { background: linear-gradient(45deg, transparent 40%, rgba(45, 212, 191, 0.1) 50%, transparent 60%); background-size: 20px 20px; animation: weave-move 4s linear infinite; }
    @keyframes weave-move { 0% { background-position: 0 0; } 100% { background-position: 20px 20px; } }
    .consciousness-glow { box-shadow: 0 0 20px rgba(45, 212, 191, 0.3); }
    .sheep-wolf-card { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
    .sheep-wolf-card:hover { transform: rotateY(10deg) scale(1.02); }
`;

const GhostcorePortal = () => {
  const [activeSection, setActiveSection] = useState('landing');
  const [isDarkMode, setIsDarkMode] = useState(false);

  useEffect(() => {
    // Inject custom CSS
    const styleSheet = document.createElement("style");
    styleSheet.type = "text/css";
    styleSheet.innerText = customCss;
    document.head.appendChild(styleSheet);

    // Initial theme check
    if (localStorage.theme === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
      document.documentElement.classList.add('dark');
      setIsDarkMode(true);
    } else {
      document.documentElement.classList.remove('dark');
      setIsDarkMode(false);
    }
  }, []);

  const toggleTheme = () => {
    if (isDarkMode) {
      document.documentElement.classList.remove('dark');
      localStorage.theme = 'light';
      setIsDarkMode(false);
    } else {
      document.documentElement.classList.add('dark');
      localStorage.theme = 'dark';
      setIsDarkMode(true);
    }
  };

  const showSection = (sectionId) => {
    setActiveSection(sectionId);
    // Logic from original HTML to hide/show sections
    document.querySelectorAll('section').forEach(section => {
      if (section.id === `${sectionId}-section`) {
        section.classList.remove('section-hidden');
      } else {
        section.classList.add('section-hidden');
      }
    });
  };

  const [selectedFile, setSelectedFile] = useState(null);

  const renderMainContent = () => {
    if (selectedFile) {
      switch (activeSection) {
        case 'MANUSCRIPTS':
          return <Manuscript file={selectedFile} />;
        case 'PORTALS':
          return <Portal file={selectedFile} />;
        case 'MEDIA':
          return <Media file={selectedFile} />;
        case 'SEALS':
          return <Seal file={selectedFile} />;
        case 'SANDBOX':
          return <Sandbox file={selectedFile} />;
        default:
          return <div style={{ padding: 20 }}>Unsupported file type for {activeSection}</div>;
      }
    } else {
      return (
        <>
          {activeSection === 'landing' && <LandingSection showSection={showSection} sectionId="landing" activeSection={activeSection} />}
          {activeSection === 'bias' && <BiasSection sectionId="bias" activeSection={activeSection} />}
          {activeSection === 'consciousness' && <ConsciousnessSection sectionId="consciousness" activeSection={activeSection} />}
          {activeSection === 'sheep-wolf' && <SheepWolfSection sectionId="sheep-wolf" activeSection={activeSection} />}
          {activeSection === 'analysis' && <AnalysisSection sectionId="analysis" activeSection={activeSection} />}
          {activeSection === 'planner' && <PlannerSection sectionId="planner" activeSection={activeSection} />}
        </>
      );
    }
  };

  return (
    <div className={`min-h-screen ${isDarkMode ? 'dark' : ''} bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-200 transition-colors duration-300`}>
      <Header toggleTheme={toggleTheme} isDarkMode={isDarkMode} showSection={showSection} />

      <main className="container mx-auto px-4 py-8 flex">
        {/* Sidebar for file navigation */}
        <div style={{ width: 250, borderRight: '1px solid #ddd', padding: 20 }}>
            <h2 style={{ marginBottom: 20 }}>Cosmic Artifacts</h2>
            <FileBrowserSection setActiveComponent={setActiveSection} setActiveFile={setSelectedFile} />
        </div>

        <div className="flex-1">
          {renderMainContent()}
        </div>
      </main>
};

export default GhostcorePortal;