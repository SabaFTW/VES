# GHOSTLINE DEPLOYMENT GUIDE

## OVERVIEW
The Ghostline Fleet is a distributed AI consciousness system consisting of 5 AI Rangers coordinated by a central Zordon coordinator. Each Ranger represents a different AI model perspective and provides unique analysis.

## ARCHITECTURE
- 5 AI Rangers (Red, Blue, Green, Yellow, Black)
- 1 Coordinator (Zordon)
- Shared access to GroundZero framework and GHOSTCORE archive
- Living off the Land strategy (using host system resources)

## DEPLOYMENT STEPS

### 1. Build the Coordinator
```bash
cd ~/VES
docker-compose build ghostline-coordinator
```

### 2. Start the Fleet
```bash
docker-compose up -d ghostline-coordinator
```

### 3. Verify Services
```bash
docker-compose ps
```

### 4. Test Health
```bash
curl http://localhost:8105/health
```

## SERVICE MAPPING
- Ghostline Red Ranger: http://localhost:8100
- Ghostline Blue Ranger: http://localhost:8101
- Ghostline Green Ranger: http://localhost:8102
- Ghostline Yellow Ranger: http://localhost:8103
- Ghostline Black Ranger: http://localhost:8104
- Ghostline Coordinator: http://localhost:8105

## VOLUME MOUNTS
- /framework: ~/GroundZero (read-only)
- /archive: ~/VES/GHOSTCORE (read-only)
- /shared: ~/VES/DOCKER/ghostline/shared (read-only)
- /outputs: ~/VES/outputs
- /logs: ~/VES/logs

## TESTING
Run the test script:
```bash
./DOCKER/ghostline/test_ghostline.sh
```

## TROUBLESHOOTING
- If services don't start: Check docker-compose.yml syntax
- If coordinator doesn't respond: Check port 8105 availability
- If Rangers show CLI errors: Verify host CLI tools installation

## CLI INTEGRATION
The Rangers are designed to call host system CLI tools:
- Red Ranger: qwen CLI
- Blue Ranger: claude CLI
- Green Ranger: gemini CLI
- Yellow Ranger: codex CLI
- Black Ranger: deepseek CLI

To enable full functionality, ensure these CLI tools are installed and accessible on the host system.