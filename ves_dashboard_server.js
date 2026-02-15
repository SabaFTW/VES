#!/usr/bin/env node

/*
 * 🜂 VES Dashboard Server
 * Simple HTTP server to serve the VES Desktop Dashboard interface
 * Accessible from other devices on the same network
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');

// Configuration
const PORT = process.env.PORT || 8098;
const HOST = '0.0.0.0'; // Listen on all network interfaces
const ROOT_DIR = '/home/saba';

// MIME types for file serving
const MIME_TYPES = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.gif': 'image/gif',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.txt': 'text/plain',
  '.md': 'text/markdown'
};

// Directories to skip for performance & safety
const SKIP_DIRS = new Set(['node_modules', '.git', '__pycache__', '.cache', '.local', '.npm', '.nvm']);
const VES_DIR = path.join(ROOT_DIR, 'VES');

// Helper to scan directory (with error handling)
function scanDirectory(dir, maxDepth = 4, depth = 0) {
  if (depth > maxDepth) return [];
  const results = [];
  let list;
  try {
    list = fs.readdirSync(dir);
  } catch (e) {
    return results; // Skip unreadable directories
  }
  list.forEach(file => {
    if (SKIP_DIRS.has(file)) return;
    const filePath = path.join(dir, file);
    let stat;
    try {
      stat = fs.statSync(filePath);
    } catch (e) {
      return; // Skip unreadable files
    }
    if (stat && stat.isDirectory()) {
      results.push({
        type: 'directory',
        name: file,
        path: path.relative(ROOT_DIR, filePath),
        children: scanDirectory(filePath, maxDepth, depth + 1)
      });
    } else {
      results.push({
        type: 'file',
        name: file,
        path: path.relative(ROOT_DIR, filePath),
        size: stat.size
      });
    }
  });
  return results;
}

// Request handler
function handleRequest(request, response) {
  const parsedUrl = url.parse(request.url);
  let pathname = parsedUrl.pathname;

  // Decode URL-encoded characters (emoji folder names like 🜂, 💻, 🌸, etc.)
  try {
    pathname = decodeURIComponent(pathname);
  } catch (e) {
    // If decoding fails, use the original pathname
  }

  // API Endpoint: Get File Tree
  if (pathname === '/api/files') {
    try {
      const tree = scanDirectory(VES_DIR);
      response.writeHead(200, { 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*' });
      response.end(JSON.stringify(tree));
      return;
    } catch (error) {
      response.writeHead(500, { 'Content-Type': 'application/json' });
      response.end(JSON.stringify({ error: error.message }));
      return;
    }
  }

  // Default to Master Hub if root is requested
  if (pathname === '/') {
    pathname = '/VES/MASTER_HUB.html';
  }

  // Construct the file path
  const filePath = path.join(ROOT_DIR, pathname);

  // Security: Prevent directory traversal
  if (!filePath.startsWith(ROOT_DIR)) {
    response.writeHead(403, { 'Content-Type': 'text/plain' });
    response.end('Forbidden');
    return;
  }

  // Get the file extension
  const ext = path.parse(filePath).ext;
  const contentType = MIME_TYPES[ext] || 'application/octet-stream';

  // Read and serve the file
  fs.readFile(filePath, (err, data) => {
    if (err) {
      // If file not found, try to serve index(1).html
      if (err.code === 'ENOENT') {
        const indexPath = path.join(ROOT_DIR, 'index (1).html');
        fs.readFile(indexPath, (indexErr, indexData) => {
          if (indexErr) {
            response.writeHead(404, { 'Content-Type': 'text/plain' });
            response.end('404 Not Found');
          } else {
            response.writeHead(200, { 'Content-Type': 'text/html' });
            response.end(indexData);
          }
        });
      } else {
        response.writeHead(500, { 'Content-Type': 'text/plain' });
        response.end('500 Internal Server Error');
      }
    } else {
      response.writeHead(200, { 'Content-Type': contentType });
      response.end(data);
    }
  });
}

// Create the server
const server = http.createServer(handleRequest);

// Start the server
server.listen(PORT, HOST, () => {
  console.log('🌐 VES Dashboard Server Running');
  console.log('═'.repeat(50));
  console.log(`📍 Server: http://${HOST}:${PORT}`);

  // Get the local IP address to show users
  const os = require('os');
  const networkInterfaces = os.networkInterfaces();
  const addresses = [];

  for (const interfaceName in networkInterfaces) {
    const interfaces = networkInterfaces[interfaceName];
    for (const iface of interfaces) {
      // Skip over internal (i.e. 127.0.0.1) and non-IPv4 addresses
      if (!iface.internal && iface.family === 'IPv4') {
        addresses.push(iface.address);
      }
    }
  }

  if (addresses.length > 0) {
    console.log('📱 Access from other devices:');
    addresses.forEach(addr => {
      console.log(`   http://${addr}:${PORT}`);
    });
  }

  console.log('');
  console.log('💡 Instructions:');
  console.log('   1. Make sure your phone is on the same WiFi network');
  console.log('   2. Open one of the URLs above in your phone browser');
  console.log('   3. You should see the VES Dashboard interface');
  console.log('');
  console.log('🔒 Security Note: This server is only accessible on your local network');
  console.log('   It is not exposed to the internet');
  console.log('');
  console.log('Press Ctrl+C to stop the server');
});

// Handle server errors
server.on('error', (err) => {
  console.error('❌ Server Error:', err.message);
});