import React from 'react';

const BiasSection = ({ sectionId, activeSection }) => {
  return (
    <section id={`${sectionId}-section`} className={activeSection === sectionId ? '' : 'section-hidden'}>
      <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-800 text-center p-4 rounded-xl mb-8 weave-pattern">
          <div className="container mx-auto px-6">
              <h1 className="text-4xl md:text-6xl font-bold text-gray-800 dark:text-gray-100 mb-2">🐺 THE BIRD ILLUSION 🐺</h1>
              <p className="text-lg md:text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
                  Izbirate stran. Destinacija je ista. <strong>Obe krili služita isti ptic!</strong><br/>
                  <em>"The sky is bigger than the bird..."</em>
              </p>
              <div id="path-selection" className="grid md:grid-cols-2 gap-8 mb-12">
                  <div className="path-choice bg-white dark:bg-gray-700 p-8 rounded-xl cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition" onClick={() => selectPath('left')}>
                      <h2 className="text-2xl font-bold mb-4 text-blue-500">🔥 LEVA POT - "PROGRESSIVE"</h2>
                      <p className="text-gray-600 dark:text-gray-300">"Sistem je pokvarjen zaradi kapitalistov! Potrebujemo več regulacije, več socialne pravičnosti, vice state control!"</p>
                      <div className="mt-4 text-sm text-blue-400">→ Hasan, AOC, mainstream left discourse</div>
                  </div>
                  <div className="path-choice bg-white dark:bg-gray-700 p-8 rounded-xl cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-600 transition" onClick={() => selectPath('right')}>
                      <h2 className="text-2xl font-bold mb-4 text-red-500">⚡ DESNA POT - "LIBERTARIAN"</h2>
                      <p className="text-gray-600 dark:text-gray-300">"Sistem je pokvarjen zaradi Big Government! Potrebujemo več svobodnih trgov, manj regulacije, individual responsibility!"</p>
                      <div className="mt-4 text-sm text-red-400">→ Charlie, Ben Shapiro, mainstream right discourse</div>
                  </div>
              </div>
              <div className="relative h-64 mb-12 hidden" id="paths-container">
                  <svg viewBox="0 0 800 400" className="w-full h-full">
                      <path className="path left-path" d="M 100,350 Q 200,50 400,200 Q 600,350 700,100" stroke="#60a5fa" strokeWidth="4" fill="none"/>
                      <path className="path right-path" d="M 100,350 Q 200,300 300,50 Q 500,100 700,100" stroke="#f87171" strokeWidth="4" fill="none"/>
                      <circle cx="700" cy="100" r="15" fill="#10b981" className="consciousness-glow"/>
                      <text x="710" y="115" fill="#10b981" className="text-sm font-bold">SAME DESTINATION</text>
                  </svg>
              </div>
              <div className="fade-in" id="result" style={{ opacity: activeSection === sectionId ? 1 : 0, transition: 'opacity 1.5s ease 3s' }}>
                  <h2 className="text-3xl font-bold text-green-500 mb-4">🎯 ISTA DESTINACIJA - BOTH WINGS, SAME BIRD!</h2>
                  <div className="bg-white dark:bg-gray-700 p-6 rounded-lg max-w-3xl mx-auto mb-6 text-left">
                      <h3 className="font-bold text-xl mb-4 text-teal-400">🔍 Pattern Recognition Activated:</h3>
                      <ul className="space-y-3 text-gray-700 dark:text-gray-300">
                          <li><strong>Left Wing:</strong> "Problem je kapitalizem!" → Solution: Więcej state power</li>
                          <li><strong>Right Wing:</strong> "Problem je government!" → Solution: Więcej corporate power</li>
                          <li><strong>Reality Check:</strong> Oba rešitvi povečata koncentracijo moči v istih rokah! 🤝</li>
                          <li><strong>The Bird:</strong> Elite networks benefit from BOTH "solutions" - they own both government AND corporations!</li>
                      </ul>
                      <div className="mt-4 p-4 bg-teal-100 dark:bg-teal-900/30 rounded border-l-4 border-teal-500">
                          <p className="text-teal-700 dark:text-teal-300 font-semibold">
                              "The predator doesn't want to win the argument. It wants to keep the argument going forever."
                          </p>
                      </div>
                  </div>
                  <button onClick={() => resetGame()} className="bg-gray-600 hover:bg-gray-700 text-white font-bold py-3 px-8 rounded-full transition">
                      Reset & See The Sky 🌌
                  </button>
              </div>
          </div>
      </div>
    </section>
  );
};

export default BiasSection;