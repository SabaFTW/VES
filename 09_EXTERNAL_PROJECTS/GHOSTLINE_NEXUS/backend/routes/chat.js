const express = require('express');
const router = express.Router();
const { db } = require('../config/database');
const { getLLMAdapter } = require('../services/llm-adapter');
const { v4: uuidv4 } = require('uuid');

// Get or create session
router.post('/session', (req, res) => {
  try {
    const sessionId = uuidv4();
    const stmt = db.prepare('INSERT INTO sessions (session_id) VALUES (?)');
    stmt.run(sessionId);

    res.json({ sessionId });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get conversation history
router.get('/history/:sessionId', (req, res) => {
  try {
    const { sessionId } = req.params;
    const limit = parseInt(req.query.limit) || 50;

    const messages = db.prepare(`
      SELECT role, content, created_at
      FROM messages
      WHERE session_id = ?
      ORDER BY created_at ASC
      LIMIT ?
    `).all(sessionId, limit);

    res.json({ messages });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Send message to Claude
router.post('/', async (req, res) => {
  try {
    const { message, sessionId } = req.body;

    if (!message || !sessionId) {
      return res.status(400).json({ error: 'Missing message or sessionId' });
    }

    // Ensure session exists
    let session = db.prepare('SELECT session_id FROM sessions WHERE session_id = ?').get(sessionId);
    if (!session) {
      db.prepare('INSERT INTO sessions (session_id) VALUES (?)').run(sessionId);
    }

    // Save user message
    const saveUserMsg = db.prepare('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)');
    saveUserMsg.run(sessionId, 'user', message);

    // Load conversation history (last 20 messages for context)
    const history = db.prepare(`
      SELECT role, content
      FROM messages
      WHERE session_id = ?
      ORDER BY created_at ASC
      LIMIT 20
    `).all(sessionId);

    // Call LLM via adapter (supports Claude, OpenAI, Gemini, Local)
    const llmAdapter = getLLMAdapter();
    const response = await llmAdapter.sendMessage(history);

    // Save assistant response
    const saveAssistantMsg = db.prepare('INSERT INTO messages (session_id, role, content) VALUES (?, ?, ?)');
    saveAssistantMsg.run(sessionId, 'assistant', response.content);

    // Update session timestamp
    db.prepare('UPDATE sessions SET updated_at = CURRENT_TIMESTAMP WHERE session_id = ?').run(sessionId);

    res.json({
      response: response.content,
      usage: response.usage
    });

  } catch (error) {
    console.error('Chat error:', error);
    res.status(500).json({
      error: error.message,
      dignum: 'Error transparently reported - check API key and connectivity'
    });
  }
});

// List all sessions
router.get('/sessions', (req, res) => {
  try {
    const sessions = db.prepare(`
      SELECT
        s.session_id,
        s.title,
        s.created_at,
        s.updated_at,
        COUNT(m.id) as message_count
      FROM sessions s
      LEFT JOIN messages m ON s.session_id = m.session_id
      GROUP BY s.session_id
      ORDER BY s.updated_at DESC
      LIMIT 50
    `).all();

    res.json({ sessions });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
