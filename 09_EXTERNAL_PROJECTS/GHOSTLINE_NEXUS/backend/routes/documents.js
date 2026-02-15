const express = require('express');
const router = express.Router();
const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { db } = require('../config/database');

// Configure multer for file uploads
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadDir = path.join(__dirname, '../storage/uploads');
    if (!fs.existsSync(uploadDir)) {
      fs.mkdirSync(uploadDir, { recursive: true });
    }
    cb(null, uploadDir);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${Date.now()}-${file.originalname}`;
    cb(null, uniqueName);
  }
});

const upload = multer({
  storage,
  limits: {
    fileSize: 10 * 1024 * 1024 // 10MB limit
  },
  fileFilter: (req, file, cb) => {
    // Check extension
    const allowedExtensions = /\.(pdf|txt|md|json|png|jpg|jpeg|gif)$/i;
    const hasValidExt = allowedExtensions.test(file.originalname);

    // Allowed mimetypes
    const allowedMimes = [
      'application/pdf',
      'text/plain',
      'text/markdown',
      'application/json',
      'image/png',
      'image/jpeg',
      'image/jpg',
      'image/gif'
    ];
    const hasValidMime = allowedMimes.includes(file.mimetype);

    // Accept if extension is valid (mimetype can be wrong for .md files)
    if (hasValidExt) {
      cb(null, true);
    } else {
      cb(new Error('Only documents (.pdf, .txt, .md, .json) and images (.png, .jpg, .gif) allowed'));
    }
  }
});

// Upload document
router.post('/', upload.single('file'), (req, res) => {
  try {
    if (!req.file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    const { name, type } = req.body;

    const stmt = db.prepare('INSERT INTO documents (name, type, file_path) VALUES (?, ?, ?)');
    const result = stmt.run(
      name || req.file.originalname,
      type || 'document',
      req.file.path
    );

    res.json({
      id: result.lastInsertRowid,
      name: name || req.file.originalname,
      type: type || 'document',
      filename: req.file.filename
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// List documents
router.get('/', (req, res) => {
  try {
    const limit = parseInt(req.query.limit) || 50;
    const type = req.query.type;

    let query = 'SELECT id, name, type, created_at FROM documents';
    let params = [];

    if (type) {
      query += ' WHERE type = ?';
      params.push(type);
    }

    query += ' ORDER BY created_at DESC LIMIT ?';
    params.push(limit);

    const documents = db.prepare(query).all(...params);
    res.json({ documents });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get document content
router.get('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const doc = db.prepare('SELECT * FROM documents WHERE id = ?').get(id);

    if (!doc) {
      return res.status(404).json({ error: 'Document not found' });
    }

    // For now, just return metadata. In production, you'd stream the file
    res.json({
      id: doc.id,
      name: doc.name,
      type: doc.type,
      created_at: doc.created_at,
      file_path: doc.file_path
    });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Delete document
router.delete('/:id', (req, res) => {
  try {
    const { id } = req.params;
    const doc = db.prepare('SELECT file_path FROM documents WHERE id = ?').get(id);

    if (!doc) {
      return res.status(404).json({ error: 'Document not found' });
    }

    // Delete file
    if (fs.existsSync(doc.file_path)) {
      fs.unlinkSync(doc.file_path);
    }

    // Delete from database
    db.prepare('DELETE FROM documents WHERE id = ?').run(id);

    res.json({ success: true });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
