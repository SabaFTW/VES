// 🜂 Simple Token Authentication Middleware
// DIGNUM: Optional protection without complex user management

const authMiddleware = (req, res, next) => {
  const authToken = process.env.AUTH_TOKEN;

  // If no auth token set, allow all requests
  if (!authToken || authToken.trim() === '') {
    return next();
  }

  // Check for token in Authorization header
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({
      error: 'Authentication required',
      dignum_note: 'Set Authorization: Bearer <token> header'
    });
  }

  const token = authHeader.substring(7); // Remove "Bearer " prefix

  if (token !== authToken) {
    return res.status(403).json({
      error: 'Invalid authentication token',
      dignum_note: 'Token does not match'
    });
  }

  // Token is valid, continue
  next();
};

module.exports = authMiddleware;
