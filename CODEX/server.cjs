const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
app.use(cors());
const port = 9001;

// Serve static files from the 'dist' directory
app.use(express.static(path.join(__dirname, 'dist')));

// Serve index.html for the root path
app.get('/', (req, res) => {
  res.sendFile(path.resolve(__dirname, 'dist', 'index.html'));
});

// Simple test endpoint
app.get('/test', (req, res) => {
  res.send('OK');
});

app.listen(port, () => {
  console.log(`Simplified PWA server listening at http://localhost:${port}`);
});