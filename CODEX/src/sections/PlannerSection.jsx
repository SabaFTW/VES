import React from 'react';

const PlannerSection = ({ sectionId, activeSection }) => {
  return (
    <section id={`${sectionId}-section`} className={activeSection === sectionId ? '' : 'section-hidden'}>
      <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-6 md:p-8 mb-8">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center">
            <svg className="w-8 h-8 text-blue-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
            <h1 className="text-3xl font-bold text-gray-800 dark:text-gray-100">Action Planner</h1>
          </div>
          <button id="suggest-task-btn" className="text-sm bg-purple-100 dark:bg-purple-900/50 text-purple-700 dark:text-purple-300 font-semibold py-2 px-4 rounded-lg hover:bg-purple-200 dark:hover:bg-purple-800/60 transition-all flex items-center gap-2">
            Suggest Next Task ✨
          </button>
        </div>
        <div id="task-form" className="flex items-center gap-3 mb-6">
          <input type="text" id="task-input" placeholder="Add a new action..." className="flex-grow bg-gray-100 dark:bg-gray-700 border-2 border-gray-200 dark:border-gray-600 rounded-lg py-3 px-4 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-gray-800 dark:text-gray-200 placeholder-gray-500 dark:placeholder-gray-400"/>
          <button type="button" onClick={() => addTask()} className="bg-blue-500 hover:bg-blue-600 text-white font-semibold py-3 px-6 rounded-lg transition shadow-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50">
            Add
          </button>
        </div>
        <ul id="task-list" className="space-y-3"></ul>
      </div>
    </section>
  );
};

export default PlannerSection;
