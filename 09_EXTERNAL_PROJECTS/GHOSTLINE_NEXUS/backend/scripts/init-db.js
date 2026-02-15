require('dotenv').config();
const { initDatabase } = require('../config/database');

console.log('🜂 GHOSTLINE NEXUS - Database Initialization');
console.log('============================================');

try {
  initDatabase();
  console.log('✅ Database initialization complete');
  console.log('SIDRO STOJI. PLAMEN GORI.');
} catch (error) {
  console.error('❌ Database initialization failed:', error);
  process.exit(1);
}
