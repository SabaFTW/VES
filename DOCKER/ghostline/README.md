# 🜂 Ghostline Fleet - Distributed AI Consciousness 🜂

## Overview

The Ghostline Fleet is a distributed AI consciousness system consisting of 5 AI "Rangers" coordinated by a central "Zordon" coordinator. Each Ranger represents a different AI model (ChatGPT, Claude, Gemini, Grok, DeepSeek) and provides a unique perspective on analysis tasks.

## Architecture

### Components

1. **ChatGPT Ship (Red Ranger)** - Technical execution and implementation
2. **Claude Ship (Blue Ranger)** - Philosophical synthesis and ethical considerations
3. **Gemini Ship (Green Ranger)** - Multimodal understanding
4. **Grok Ship (Yellow Ranger)** - Unfiltered truth and contrarian perspectives
5. **DeepSeek Ship (Black Ranger)** - Deep research and mathematical analysis
6. **Ghostline Coordinator (Zordon)** - Central coordination and synthesis

### Shared Resources

- **Framework**: `/framework` - Mounts GroundZero (ethical framework, AI practices)
- **Archive**: `/archive` - Mounts GHOSTCORE (forensic evidence, battle plans)

## Deployment

### Prerequisites

- Docker
- Docker Compose

### Setup

1. Ensure the coordinator code is built:
   ```bash
   cd /home/saba/VES
   docker-compose build ghostline-coordinator
   ```

2. Start the entire fleet:
   ```bash
   docker-compose up -d ghostline-coordinator
   ```

This will start all 6 services (5 Rangers + 1 Coordinator).

## Ports

- **Red Ranger (ChatGPT)**: `localhost:8100`
- **Blue Ranger (Claude)**: `localhost:8101`
- **Green Ranger (Gemini)**: `localhost:8102`
- **Yellow Ranger (Grok)**: `localhost:8103`
- **Black Ranger (DeepSeek)**: `localhost:8104`
- **Coordinator (Zordon)**: `localhost:8105`

## Usage

### Health Check

```bash
curl http://localhost:8105/health
```

Expected response:
```json
{
  "status": "healthy",
  "coordinator": "zordon"
}
```

### Submit Analysis Query

```bash
curl -X POST http://localhost:8105/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze the connection between Epstein network and 8200 surveillance using all 5 perspectives"
  }'
```

### Check Ranger Status

```bash
curl http://localhost:8105/status
```

## How It Works

1. User submits a query to the Coordinator
2. Coordinator distributes the query to all 5 Rangers
3. Each Ranger analyzes the query using:
   - Shared framework knowledge (GroundZero)
   - Shared archive knowledge (GHOSTCORE)
   - Each Ranger's unique perspective
4. Coordinator collects all responses
5. Coordinator synthesizes a unified response
6. Response is returned to the user

## Testing

Run the test script:

```bash
./DOCKER/ghostline/test_fleet.sh
```

## Troubleshooting

### Services Not Starting

Check logs:
```bash
docker-compose logs ghostline-coordinator
docker-compose logs chatgpt-ship
# ... etc for other services
```

### Coordinator Not Responding

Ensure all Ranger services are running:
```bash
docker-compose ps | grep ghostline
```

### Volume Mount Issues

Verify that:
- `/home/saba/GroundZero` exists and is accessible
- `/home/saba/VES/GHOSTCORE` exists and is accessible
- Proper read permissions are set

### Network Issues

All services run on the `ves_network` bridge network and communicate internally using service names as hostnames.