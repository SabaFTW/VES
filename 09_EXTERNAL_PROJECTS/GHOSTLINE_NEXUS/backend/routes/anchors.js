const express = require('express');
const router = express.Router();
const { db } = require('../config/database');

// Create anchor
router.post('/', (req, res) => {
  try {
    const { type, name, data, file_path } = req.body;

    if (!type || !name) {
      return res.status(400).json({ error: 'Type and name required' });
    }

    if (!['sigil', 'qr', 'project'].includes(type)) {
      return res.status(400).json({ error: 'Invalid anchor type' });
    }

    const stmt = db.prepare('INSERT INTO anchors (type, name, data, file_path) VALUES (?, ?, ?, ?)');
    const result = stmt.run(type, name, data, file_path);

    res.json({
      id: result.lastInsertRowid,
      type,
      name
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// List anchors
router.get('/', (req, res) => {
  try {
    const type = req.query.type;
    const limit = parseInt(req.query.limit) || 50;

    let query = 'SELECT * FROM anchors';
    let params = [];

    if (type) {
      query += ' WHERE type = ?';
      params.push(type);
    }

    query += ' ORDER BY created_at DESC LIMIT ?';
    params.push(limit);

    const anchors = db.prepare(query).all(...params);
    res.json({ anchors });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get specific anchor
router.get('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const anchor = db.prepare('SELECT * FROM anchors WHERE id = ?').get(id);

    if (!anchor) {
      return res.status(404).json({ error: 'Anchor not found' });
    }

    res.json(anchor);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Update anchor
router.put('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const { name, data, file_path } = req.body;

    const updates = [];
    const params = [];

    if (name) {
      updates.push('name = ?');
      params.push(name);
    }
    if (data) {
      updates.push('data = ?');
      params.push(data);
    }
    if (file_path) {
      updates.push('file_path = ?');
      params.push(file_path);
    }

    if (updates.length === 0) {
      return res.status(400).json({ error: 'No fields to update' });
    }

    params.push(id);
    const query = `UPDATE anchors SET ${updates.join(', ')} WHERE id = ?`;

    db.prepare(query).run(...params);

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete anchor
router.delete('/:id', (req, res) => {
  try {
    const { id } = req.params;
    db.prepare('DELETE FROM anchors WHERE id = ?').run(id);
    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
