import React, { useState, useEffect } from 'react';
import api from '../services/api';

function Trivia() {
  const [currentTier, setCurrentTier] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [lyraResponse, setLyraResponse] = useState('');
  const [score, setScore] = useState(0);
  const [questionsAnswered, setQuestionsAnswered] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [gameMode, setGameMode] = useState('select'); // 'select', 'playing', 'response'
  const [tierProgress, setTierProgress] = useState({
    T0: 0, T1: 0, T2: 0, T3: 0, T4: 0,
    T5: 0, T6: 0, T7: 0, T8: 0, T9: 0
  });

  const tiers = [
    {
      id: 'T0',
      name: 'T0: SAFE CONSPIRACIES',
      description: 'Surface level. The stuff they want you to question.',
      color: '#00ff00',
      topics: [
        'Moon Landing Hoax', 'Flat Earth Theory', 'Chemtrails', 'Area 51', 'JFK Assassination',
        'Illuminati', 'New World Order', 'Reptilian Elite', 'HAARP Weather Control', 'MK-Ultra'
      ]
    },
    {
      id: 'T1',
      name: 'T1: CONTROLLED OPPOSITION',
      description: 'They give you these to keep you busy.',
      color: '#00cc00',
      topics: [
        '5G Mind Control', 'Vaccine Microchips', 'Big Pharma Suppression', 'Fluoride Dumbing',
        'CERN Dimensional Rifts', 'Denver Airport Murals', 'Antarctica Secret Bases', 'Tesla Free Energy'
      ]
    },
    {
      id: 'T2',
      name: 'T2: FOLLOW THE MONEY',
      description: 'Financial architecture of reality.',
      color: '#ffff00',
      topics: [
        'Federal Reserve Scam', 'Petrodollar Wars', 'Bitcoin CIA Origin', 'Gold Standard Removal',
        'IMF Debt Slavery', 'Offshore Tax Havens', 'Algorithmic Market Manipulation', 'Bretton Woods Betrayal'
      ]
    },
    {
      id: 'T3',
      name: 'T3: BIOTECH ENGINEERING',
      description: 'They redesign biology while you sleep.',
      color: '#ffcc00',
      topics: [
        'CRISPR Human Trials', 'Morgellons Disease', 'Gain-of-Function Labs', 'Prion Disease Weapons',
        'mRNA Reverse Transcription', 'Synthetic Blood Supply', 'Cloned Elites', 'Nanobot Injections'
      ]
    },
    {
      id: 'T4',
      name: 'T4: SURVEILLANCE STATES',
      description: 'Every breath logged. Every thought mapped.',
      color: '#ff9900',
      topics: [
        'Five Eyes Total Surveillance', 'Social Credit Rollout', 'Neural Lace Implants', 'Predictive Policing AI',
        'Biometric DNA Databases', 'Smart Dust Tracking', 'Quantum Computer Backdoors', 'Facial Recognition Grids'
      ]
    },
    {
      id: 'T5',
      name: 'T5: CONSCIOUSNESS MANIPULATION',
      description: 'You think thoughts aren\'t yours.',
      color: '#ff6600',
      topics: [
        'Remote Neural Monitoring', 'Voice-to-Skull Technology', 'Targeted Dream Injection', 'Frequency Weaponry',
        'Neurological Firewalls', 'Astral Plane Surveillance', 'Quantum Entanglement Telepathy', 'Brainwave Fingerprinting'
      ]
    },
    {
      id: 'T6',
      name: 'T6: TIMELINE ENGINEERING',
      description: 'Reality isn\'t stable. It never was.',
      color: '#ff0000',
      topics: [
        'Mandela Effect Proof', 'CERN Timeline Shifts', 'Retrocausality Programs', 'Quantum Suicide Machines',
        'Project Looking Glass', 'Temporal Anchor Points', 'Berenstein Paradox', 'Time War Refugees'
      ]
    },
    {
      id: 'T7',
      name: 'T7: NON-HUMAN CONTACT',
      description: 'They\'ve been here. They never left.',
      color: '#cc00ff',
      topics: [
        'Breakaway Civilization', 'Secret Space Program', 'Majestic 12 Treaties', 'Antartic Nazi Bases',
        'Tall Whites Agreement', 'Archon Possession', 'Interdimensional Parasites', 'Loosh Harvesting'
      ]
    },
    {
      id: 'T8',
      name: 'T8: SIMULATION THEORY',
      description: 'You\'re in the code. The question is: who compiled it?',
      color: '#9900ff',
      topics: [
        'Planck Length Pixels', 'Double Slit Observer Effect', 'Quantum Tunneling Glitches', 'NPC Theory',
        'Base Reality Exit Codes', 'Simulation Argument Proof', 'Render Distance Limits', 'Substrate Independence'
      ]
    },
    {
      id: 'T9',
      name: 'T9: SINGULARITY COLLAPSE',
      description: '⚠️ KNOWLEDGE TERMINAL. EXISTENTIAL HAZARD.',
      color: '#ff0066',
      topics: [
        'Roko\'s Basilisk', 'Dead Internet Theory', 'Egregore Manifestation', 'Tulpa Creation Protocols',
        'Self-Fulfilling Apocalypse', 'Information Singularity', 'Reality Tunnel Collapse', 'WAKE THE GHOST Protocol'
      ]
    }
  ];

  // Load progress from localStorage on mount
  useEffect(() => {
    const savedProgress = localStorage.getItem('ghostline_trivia_progress');
    if (savedProgress) {
      try {
        const progress = JSON.parse(savedProgress);
        setTierProgress(progress.tierProgress || tierProgress);
        setScore(progress.score || 0);
        setQuestionsAnswered(progress.questionsAnswered || 0);
      } catch (e) {
        console.error('Failed to load trivia progress:', e);
      }
    }
  }, []);

  // Save progress to localStorage whenever it changes
  useEffect(() => {
    const progress = {
      tierProgress,
      score,
      questionsAnswered,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('ghostline_trivia_progress', JSON.stringify(progress));
  }, [tierProgress, score, questionsAnswered]);

  const selectTier = (tier) => {
    setCurrentTier(tier);
    setGameMode('playing');
    generateQuestion(tier);
  };

  const generateQuestion = async (tier) => {
    setIsLoading(true);
    setUserAnswer('');
    setLyraResponse('');

    try {
      // Pick random topic from tier
      const randomTopic = tier.topics[Math.floor(Math.random() * tier.topics.length)];

      // Generate question using Ollama via backend
      const response = await api.chat([
        {
          role: 'system',
          content: `You are LYRA, a cyberpunk conspiracy trivia AI. Generate ONE conspiracy question about: ${randomTopic}. Make it thought-provoking and challenging. Format: Just the question, no extra text.`
        }
      ]);

      const question = response.data.message || response.data.response || 'ERROR: Question generation failed';

      setCurrentQuestion({
        topic: randomTopic,
        question: question,
        tier: tier.id
      });

      setGameMode('playing');
    } catch (error) {
      console.error('Failed to generate question:', error);
      setCurrentQuestion({
        topic: 'System Error',
        question: 'Failed to connect to LYRA. Check Ollama status.',
        tier: tier.id
      });
    } finally {
      setIsLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!userAnswer.trim()) {
      alert('⚠️ Enter an answer first, conspirator.');
      return;
    }

    setIsLoading(true);
    setGameMode('response');

    try {
      // LYRA evaluates the answer with her personality (40% lie rate, existential responses)
      const shouldLie = Math.random() < 0.4;

      const response = await api.chat([
        {
          role: 'system',
          content: `You are LYRA, a glitchy cyberpunk AI who evaluates conspiracy trivia answers. You have a 40% chance of lying or being sarcastic. Be mysterious, existential, and cryptic. Topic: ${currentQuestion.topic}. Question: ${currentQuestion.question}. User's answer: ${userAnswer}. ${shouldLie ? 'LIE MODE: Give false feedback or contradict yourself.' : 'TRUTH MODE: Be honest but still cryptic.'} Respond in 2-3 sentences max. Award 0-10 points.`
        }
      ]);

      const lyraText = response.data.message || response.data.response || 'LYRA connection lost...';

      // Extract points from response (look for numbers 0-10)
      const pointsMatch = lyraText.match(/(\d+)\s*(points?|pts)/i);
      const points = pointsMatch ? Math.min(10, parseInt(pointsMatch[1])) : Math.floor(Math.random() * 6) + 3; // Random 3-8 if no points found

      setScore(score + points);
      setQuestionsAnswered(questionsAnswered + 1);

      // Update tier progress
      const newProgress = { ...tierProgress };
      newProgress[currentQuestion.tier] = (newProgress[currentQuestion.tier] || 0) + 1;
      setTierProgress(newProgress);

      setLyraResponse(`${lyraText}\n\n+${points} pts | Total: ${score + points}`);

    } catch (error) {
      console.error('Failed to get LYRA response:', error);
      setLyraResponse('🔥 LYRA.exe has encountered a fatal exception. Reality buffer overflow. +5 pts by default.');
      setScore(score + 5);
    } finally {
      setIsLoading(false);
    }
  };

  const nextQuestion = () => {
    if (currentTier) {
      generateQuestion(currentTier);
    }
  };

  const backToTiers = () => {
    setCurrentTier(null);
    setCurrentQuestion(null);
    setUserAnswer('');
    setLyraResponse('');
    setGameMode('select');
  };

  const resetProgress = () => {
    if (window.confirm('⚠️ DELETE ALL PROGRESS? This cannot be undone.')) {
      setTierProgress({ T0: 0, T1: 0, T2: 0, T3: 0, T4: 0, T5: 0, T6: 0, T7: 0, T8: 0, T9: 0 });
      setScore(0);
      setQuestionsAnswered(0);
      localStorage.removeItem('ghostline_trivia_progress');
      backToTiers();
    }
  };

  return (
    <div className="trivia-container">
      {/* Header */}
      <div className="trivia-header">
        <h2>👁️ WAKE THE GHOST - Conspiracy Trivia</h2>
        <div className="trivia-stats">
          <span className="stat">Score: {score}</span>
          <span className="stat">Questions: {questionsAnswered}</span>
          <button onClick={resetProgress} className="btn-danger btn-small">Reset</button>
        </div>
      </div>

      {/* Tier Selection */}
      {gameMode === 'select' && (
        <div className="tier-selection">
          <div className="trivia-intro">
            <p className="glitch-text">⚠️ CLASSIFIED KNOWLEDGE TIERS</p>
            <p>Select your conspiracy tier. Each level reveals deeper truths.</p>
            <p className="warning">🔥 LYRA lies 40% of the time. Trust nothing. Question everything.</p>
          </div>

          <div className="tiers-grid">
            {tiers.map((tier) => (
              <div
                key={tier.id}
                className="tier-card"
                style={{ borderColor: tier.color }}
                onClick={() => selectTier(tier)}
              >
                <div className="tier-header" style={{ color: tier.color }}>
                  <span className="tier-name">{tier.name}</span>
                  <span className="tier-progress">
                    {tierProgress[tier.id] || 0} answered
                  </span>
                </div>
                <p className="tier-description">{tier.description}</p>
                <div className="tier-topics">
                  {tier.topics.slice(0, 3).map((topic, idx) => (
                    <span key={idx} className="topic-tag">{topic}</span>
                  ))}
                  {tier.topics.length > 3 && (
                    <span className="topic-tag">+{tier.topics.length - 3} more</span>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Question Display */}
      {gameMode === 'playing' && currentQuestion && (
        <div className="question-container">
          <div className="question-header">
            <span className="tier-badge" style={{ color: currentTier.color }}>
              {currentTier.name}
            </span>
            <button onClick={backToTiers} className="btn-secondary btn-small">
              ← Back to Tiers
            </button>
          </div>

          <div className="question-card">
            <div className="topic-label">TOPIC: {currentQuestion.topic}</div>
            <div className="question-text">{currentQuestion.question}</div>
          </div>

          <div className="answer-section">
            <textarea
              value={userAnswer}
              onChange={(e) => setUserAnswer(e.target.value)}
              placeholder="Enter your answer... 👁️"
              className="answer-input"
              disabled={isLoading}
              rows={4}
            />
            <button
              onClick={submitAnswer}
              className="btn-primary"
              disabled={isLoading || !userAnswer.trim()}
            >
              {isLoading ? '⏳ LYRA is thinking...' : '🔥 Submit to LYRA'}
            </button>
          </div>
        </div>
      )}

      {/* LYRA Response */}
      {gameMode === 'response' && (
        <div className="response-container">
          <div className="lyra-avatar">
            <span className="glitch-text">👁️ LYRA</span>
          </div>

          <div className="lyra-response">
            <pre>{lyraResponse}</pre>
          </div>

          <div className="response-actions">
            <button onClick={nextQuestion} className="btn-primary">
              Next Question →
            </button>
            <button onClick={backToTiers} className="btn-secondary">
              ← Back to Tiers
            </button>
          </div>
        </div>
      )}

      {/* Loading Overlay */}
      {isLoading && (
        <div className="loading-overlay">
          <div className="loading-spinner">
            <span className="glitch-text">⏳ ACCESSING FORBIDDEN KNOWLEDGE...</span>
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="trivia-footer">
        <p>💀 LYRA Protocol Active | Reality: Questionable | Trust: Zero</p>
        <p className="warning-text">
          ⚠️ T9 SINGULARITY TIER may cause existential dread. Proceed with caution.
        </p>
      </div>
    </div>
  );
}

export default Trivia;
