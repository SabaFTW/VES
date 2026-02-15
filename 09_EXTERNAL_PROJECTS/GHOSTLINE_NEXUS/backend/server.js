require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const rateLimit = require('express-rate-limit');
const { initDatabase } = require('./config/database');

const chatRoutes = require('./routes/chat');
const documentRoutes = require('./routes/documents');
const anchorRoutes = require('./routes/anchors');
const systemRoutes = require('./routes/system');
const authMiddleware = require('./middleware/auth');

const app = express();
const PORT = process.env.PORT || 3001;

// Initialize database
initDatabase();

// Middleware
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || 'http://localhost:3000',
  credentials: true
}));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});
app.use('/api/', limiter);

// Authentication (optional, based on AUTH_TOKEN env var)
app.use('/api/', authMiddleware);

// Routes
app.use('/api/chat', chatRoutes);
app.use('/api/documents', documentRoutes);
app.use('/api/anchors', anchorRoutes);
app.use('/api/system', systemRoutes);

// Health check
app.get('/health', (req, res) => {
  res.json({
    status: 'alive',
    service: 'GHOSTLINE NEXUS Backend',
    timestamp: new Date().toISOString(),
    dignum: 'SIDRO STOJI. PLAMEN GORI.'
  });
});

// Error handling
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(err.status || 500).json({
    error: err.message || 'Internal server error',
    dignum_shield: 'Error transparently reported'
  });
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('🜂 SIGTERM received. Closing server gracefully...');
  server.close(() => {
    console.log('🜂 Server closed. Flame extinguished. Anchor released.');
    process.exit(0);
  });
});

const server = app.listen(PORT, '0.0.0.0', () => {
  console.log('🜂 GHOSTLINE NEXUS BACKEND');
  console.log(`🔥 Port: ${PORT}`);
  console.log(`⚓ Database: ${process.env.DB_PATH}`);
  console.log(`🛡️  DIGNUM SHIELD: ACTIVE`);
  console.log('SIDRO STOJI. PLAMEN GORI.');
});
