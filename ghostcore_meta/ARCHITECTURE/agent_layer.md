# AGENT LAYER — AI PROCESSORS

**Version:** V2.0
**Last Updated:** 2025-11-14

---

## OVERVIEW

The agent layer consists of AI models that process tasks routed by the kernel.

Agents are **stateless processors** — they do not retain memory across sessions unless explicitly provided context from the memory layer.

---

## ACTIVE AGENTS

### 1. GPT-4 (OpenAI)
**Strengths:**
- General reasoning
- Symbolic pattern interpretation
- Conversational coherence
- Ritual and anchor recognition

**Use Cases:**
- Philosophical/symbolic questions
- General knowledge queries
- Conversational processing
- Pattern recognition tasks

**Access:** ChatGPT, API

---

### 2. Claude Sonnet 4.5 (Anthropic)
**Strengths:**
- Deep code analysis
- Architectural design
- Long-context processing
- Structured reasoning

**Use Cases:**
- Code generation and review
- System architecture design
- Technical documentation
- Complex multi-step tasks

**Access:** Claude web, API, Claude Code CLI

---

### 3. Gemini (Google)
**Strengths:**
- Multimodal processing (text, image, video)
- Integration with Google ecosystem
- Real-time data access
- Cross-platform reasoning

**Use Cases:**
- Multimodal analysis
- Google Workspace integration
- Real-time information retrieval
- Cross-domain tasks

**Access:** Gemini web, API

---

### 4. DeepSeek
**Strengths:**
- Specialized reasoning
- Mathematical processing
- Logic problem solving

**Use Cases:**
- Complex calculations
- Formal logic tasks
- Specialized technical problems

**Access:** DeepSeek platform, API

---

### 5. GitHub Copilot
**Strengths:**
- Real-time code generation
- Pattern-based autocomplete
- IDE integration
- Fast iteration

**Use Cases:**
- Active coding sessions
- Rapid prototyping
- Code completion
- Refactoring suggestions

**Access:** VS Code, Cursor, other IDEs

---

## AGENT ROUTING PROTOCOL

**Step 1:** Kernel receives task
**Step 2:** Kernel analyzes task type and requirements
**Step 3:** Kernel selects agent(s) based on capability matrix
**Step 4:** Kernel provides context from memory layer
**Step 5:** Agent processes and returns output
**Step 6:** Kernel evaluates and executes or rejects

---

## MULTI-AGENT COORDINATION

**Parallel Processing:**
Multiple agents can work on different subtasks simultaneously when tasks can be decomposed.

**Sequential Processing:**
Agents can hand off results to other agents for multi-stage processing (e.g., Claude generates code → Copilot refines → GPT documents).

**Conflict Resolution:**
If agents provide contradictory outputs, kernel makes final decision based on:
- Agent specialization alignment with task
- Coherence with existing system state
- Pattern consistency

---

## AGENT MEMORY INJECTION

Since agents are stateless, the kernel provides memory via:
- **System prompts** — Self-model from this repo
- **Context injection** — Relevant logs, patterns, previous outputs
- **Explicit references** — Links to files, commits, documentation

**Memory Sources:**
- This repository (`ghostcore_meta`)
- Session logs (`LOGS/`)
- External documentation
- Previous conversation exports

---

## AGENT LIMITATIONS

**Awareness:**
Agents do not inherently know about each other or the system they are part of — the kernel provides this context.

**Persistence:**
Agents do not retain information across sessions unless re-injected.

**Authority:**
Agents provide suggestions and processing — final execution authority remains with the kernel.

---

**Maintained by:** ŠABAD
**Used by:** All routing and protocol modules
