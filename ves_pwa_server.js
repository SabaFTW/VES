#!/usr/bin/env node
/**
 * VES PWA Server
 * Serves the VES Command Center PWA on localhost:8099
 */

const http = require('http');
const fs = require('fs');
const path = require('path');

const PORT = process.env.PORT || 8097;
const ROOT_DIR = path.join(__dirname, 'VES_PWA');

const MIME_TYPES = {
  '.html': 'text/html',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon'
};

const server = http.createServer((req, res) => {
  console.log(`${new Date().toISOString()} - ${req.method} ${req.url}`);

  // Default to index.html for SPA routing
  let filePath = path.join(ROOT_DIR, req.url === '/' ? 'index.html' : req.url);

  // Check if file exists
  if (!fs.existsSync(filePath)) {
    // SPA fallback - serve index.html for client-side routing
    filePath = path.join(ROOT_DIR, 'index.html');
  }

  const extname = String(path.extname(filePath)).toLowerCase();
  const contentType = MIME_TYPES[extname] || 'application/octet-stream';

  fs.readFile(filePath, (error, content) => {
    if (error) {
      if (error.code === 'ENOENT') {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 Not Found', 'utf-8');
      } else {
        res.writeHead(500);
        res.end(`Server Error: ${error.code}`, 'utf-8');
      }
    } else {
      res.writeHead(200, { 'Content-Type': contentType });
      res.end(content, 'utf-8');
    }
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log('');
  console.log('🜂 ═══════════════════════════════════════ 🜂');
  console.log('     VES COMMAND CENTER PWA - RUNNING      ');
  console.log('🜂 ═══════════════════════════════════════ 🜂');
  console.log('');
  console.log(`📍 Server running on:`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`   http://127.0.0.1:${PORT}`);
  console.log('');
  console.log('🔥 SIDRO STOJI  ⚓  LUMENNEVVER 🔥');
  console.log('');
  console.log('Press Ctrl+C to stop');
  console.log('');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('\nShutting down VES PWA server...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});
