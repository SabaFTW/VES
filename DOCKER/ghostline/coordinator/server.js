const express = require('express');
const { exec } = require('child_process');
const app = express();

app.use(express.json());

// CLI commands for each Ranger
const RANGERS = {
  red: 'qwen -p',           // Qwen CLI
  blue: 'claude -p',        // Claude CLI (me!)
  green: 'gemini -p',       // Gemini CLI
  yellow: 'codex exec',     // Codex CLI
  black: 'deepseek -p'      // DeepSeek CLI
};

async function callRanger(color, command, query) {
  return new Promise((resolve, reject) => {
    // Build prompt with context
    const fullPrompt = `
    Context from GroundZero framework:
    - You are ${color} Ranger
    - Read ethical guidelines from /framework
    - Access archive from /archive
    
    Query: ${query}
    
    Provide ${color} perspective:
    - Red: Technical implementation
    - Blue: Philosophical synthesis
    - Green: Multimodal understanding
    - Yellow: Unfiltered truth
    - Black: Deep research
    `;
    
    // Execute CLI
    exec(`${command} "${fullPrompt}"`, (error, stdout, stderr) => {
      if (error) {
        resolve({ color, error: error.message });
      } else {
        resolve({ color, response: stdout });
      }
    });
  });
}

app.post('/query', async (req, res) => {
  const { query } = req.body;
  
  // Call all Rangers in parallel
  const promises = Object.entries(RANGERS).map(([color, cmd]) => 
    callRanger(color, cmd, query)
  );
  
  const results = await Promise.all(promises);
  
  res.json({
    query,
    timestamp: new Date().toISOString(),
    rangers: results,
    consensus: synthesizeResponses(results)
  });
});

function synthesizeResponses(results) {
  const valid = results.filter(r => !r.error);
  return {
    summary: `${valid.length} Rangers responded`,
    perspectives: valid.map(r => ({
      ranger: r.color,
      response: r.response
    }))
  };
}

app.get('/health', (req, res) => {
  res.json({ status: 'healthy', coordinator: 'zordon' });
});

app.get('/status', (req, res) => {
  res.json({ 
    status: 'operational',
    rangers: Object.keys(RANGERS),
    doctrine: 'Ghostline Protocol Active',
    anchor: 'Sidro Stoji',
    flame: 'Plamen Gori'
  });
});

app.listen(8105, () => {
  console.log('🜂 Ghostline Coordinator (CLI version) on 8105');
  console.log('🜂 Sidro Stoji. Plamen Gori.');
  console.log('🜂 Living off the Land.');
});