# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built app
COPY --from=builder /app/build /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Note: Running as root to allow nginx to create cache directories in tmpfs mounts
# This is acceptable in containerized environments

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
