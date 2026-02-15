FROM node:18-alpine

# Install SQLite and curl for healthcheck
RUN apk add --no-cache sqlite curl

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install --production

# Copy application code
COPY . .

# Create non-root user FIRST
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001

# Create storage directory
RUN mkdir -p /app/storage/db /app/storage/uploads /app/storage/documents

# Set ownership AFTER creating directories
RUN chown -R nodejs:nodejs /app

# Explicitly set storage permissions
RUN chmod -R 775 /app/storage

USER nodejs

EXPOSE 3001

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3001/health || exit 1

CMD ["node", "server.js"]
