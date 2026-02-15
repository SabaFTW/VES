import React from 'react';

const SheepWolfSection = ({ sectionId, activeSection }) => {
  return (
    <section id={`${sectionId}-section`} className={activeSection === sectionId ? '' : 'section-hidden'}>
      <div className="bg-white dark:bg-gray-800 rounded-xl p-8 mb-8">
        <h2 className="text-4xl font-bold text-center mb-6">🐑➡️🐺 SHEEP IN WOLF'S CLOTHING DETECTOR</h2>
        <p className="text-xl text-gray-600 dark:text-gray-400 text-center mb-8 max-w-3xl mx-auto">
          Learn to recognize how power structures hide behind legitimate facades. 
          <strong>Pattern: Associate with the sacred/progressive → Use that legitimacy to mask control agenda</strong>
        </p>
        
        <div className="grid md:grid-cols-3 gap-6 mb-8">
          <div className="sheep-wolf-card bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
            <h3 className="text-xl font-bold mb-4 text-amber-600">🏛️ HISTORICAL EXAMPLES</h3>
            <div className="space-y-3 text-sm">
              <div className="border-l-4 border-amber-500 pl-3">
                <strong>Knights Templar (1119-1312)</strong><br/>
                <span className="text-gray-600 dark:text-gray-400">Sheep: "Holy protectors of pilgrims"</span><br/>
                <span className="text-red-600">Wolf: Banking empire, political manipulation</span>
              </div>
              <div className="border-l-4 border-amber-500 pl-3">
                <strong>Medici Bank (1397-1494)</strong><br/>
                <span className="text-gray-600 dark:text-gray-400">Sheep: "Renaissance patrons, art supporters"</span><br/>
                <span className="text-red-600">Wolf: Political control through debt, pope-making</span>
              </div>
            </div>
          </div>
          
          <div className="sheep-wolf-card bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
            <h3 className="text-xl font-bold mb-4 text-blue-600">🏢 MODERN EXAMPLES</h3>
            <div className="space-y-3 text-sm">
              <div className="border-l-4 border-blue-500 pl-3">
                <strong>Tech Platforms</strong><br/>
                <span className="text-gray-600 dark:text-gray-400">Sheep: "Connecting people, free speech"</span><br/>
                <span className="text-red-600">Wolf: Attention harvesting, behavioral control</span>
              </div>
              <div className="border-l-4 border-blue-500 pl-3">
                <strong>"Philanthropic" Organizations</strong><br/>
                <span className="text-gray-600 dark:text-gray-400">Sheep: "Solving world problems"</span><br/>
                <span className="text-red-600">Wolf: Policy influence, tax avoidance, reputation washing</span>
              </div>
            </div>
          </div>
          
          <div className="sheep-wolf-card bg-gray-50 dark:bg-gray-700 p-6 rounded-lg">
            <h3 className="text-xl font-bold mb-4 text-green-600">🔍 DETECTION METHODS</h3>
            <div className="space-y-2 text-sm">
              <div className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Follow the money - who benefits?</span>
              </div>
              <div className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Check actions vs. stated values</span>
              </div>
              <div className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Look for regulatory capture patterns</span>
              </div>
              <div className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Identify revolving door relationships</span>
              </div>
              <div className="flex items-start">
                <span className="text-green-500 mr-2">✓</span>
                <span>Analyze who gets silenced/promoted</span>
              </div>
            </div>
          </div>
        </div>
        
        <div className="bg-red-100 dark:bg-red-900/30 p-6 rounded-lg border-l-4 border-red-500">
          <h4 className="text-xl font-bold mb-3 text-red-700 dark:text-red-400">⚠️ THE ULTIMATE SHEEP-IN-WOLF'S TRICK</h4>
          <p className="text-red-800 dark:text-red-300 mb-3">
            <strong>They make you think you're choosing sides, when both sides serve the same master.</strong>
          </p>
          <p className="text-gray-700 dark:text-gray-300">
            Left vs Right, Progressive vs Conservative, Regulation vs Free Market - 
            all these "choices" often lead to more concentration of power in the same elite networks 
            who own both government institutions AND major corporations.
          </p>
        </div>
      </div>
    </section>
  );
};

export default SheepWolfSection;
