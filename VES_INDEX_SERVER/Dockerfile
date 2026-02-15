FROM node:18-slim

WORKDIR /app

COPY package*.json ./
RUN npm install --production

COPY . .

ENV PORT=4500
EXPOSE 4500

CMD ["node", "server.js"]
