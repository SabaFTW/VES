import React from 'react';

const AnalysisSection = ({ sectionId, activeSection }) => {
  return (
    <section id={`${sectionId}-section`} className={activeSection === sectionId ? '' : 'section-hidden'}>
      <div className="bg-white dark:bg-gray-800 rounded-xl p-6 md:p-8 mb-8">
        <h2 className="text-3xl font-bold text-center mb-6">📊 Analiza: Strateški Obveščevalni Poročevalec</h2>
        <p className="text-gray-600 dark:text-gray-400 mb-8 text-center max-w-3xl mx-auto">
          Vnesi ime korporacije, tehnologije ali koncepta, in GHOSTCORE analitik bo ustvaril strateško poročilo o njegovem vplivu na družbo, moč in ideologijo.
        </p>
        <div className="max-w-2xl mx-auto">
          <textarea id="analysis-input" className="w-full p-3 border border-gray-300 rounded-lg focus:ring-accent-color focus:border-accent-color dark:bg-gray-700 dark:border-gray-600 dark:text-gray-200" rows="2" placeholder="Npr. 'Neuralink', 'TikTok algoritem', 'BlackRock'..."></textarea>
          <button id="generate-analysis-btn" className="mt-4 w-full bg-accent-color text-white font-bold py-3 px-8 rounded-full hover:bg-teal-700 dark:hover:bg-teal-500 transition transform hover:scale-105 flex items-center justify-center disabled:opacity-50">
            <span id="analysis-button-text">Generiraj Poročilo ✨</span>
            <div id="analysis-loading-spinner" className="loader hidden ml-3"></div>
          </button>
          <div id="analysis-response" className="hidden mt-6 p-4 border-l-4 border-accent-color bg-gray-50 dark:bg-gray-700/50 rounded-r-lg"></div>
        </div>
      </div>
    </section>
  );
};

export default AnalysisSection;
