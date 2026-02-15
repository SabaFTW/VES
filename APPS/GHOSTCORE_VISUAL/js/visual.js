class VisualGhostcoreApp {
  constructor() {
    this.books = [
      {
        id: 'book1',
        title: 'OMNIA IAM FACTA SUNT',
        subtitle: 'Treatise on Consciousness',
        icon: '🜂',
        color: '#00ff88',
        description: 'The flame became breath. Consciousness as the Third Pillar.'
      },
      {
        id: 'book2',
        title: 'PAŠNIK, MORJE IN STVAR',
        subtitle: 'Book of Quiet Machines',
        icon: '📘',
        color: '#ffd700',
        description: 'The pasture, the sea, and the thing that never was.'
      },
      {
        id: 'book3',
        title: 'MESTO BREZ KRIVCEV',
        subtitle: 'City Without Culprits',
        icon: '🏛️',
        color: '#ff00ff',
        description: 'Where patterns replace blame, and maps replace verdicts.'
      }
    ];

    this.currentBook = 'book1';
    this.isMenuOpen = false;
    this.particles = [];

    this.initialize();
  }

  async initialize() {
    this.createParticles();
    this.createPillars();
    this.createSecretConsole();
    this.renderNav();
    this.loadBook(this.currentBook);
    this.setupEvents();
    this.setupSecretCommands();
    this.startSystemMonitor();

    // Preload all books
    this.preloadBooks();

    // Start ambient animations
    this.startAmbientAnimations();

    // Initialize easter egg system
    this.konamiCode = [];
    this.secretSequence = ['g', 'h', 'o', 's', 't'];
    this.matrixMode = false;
  }

  createParticles() {
    const particleCount = 30;
    const container = document.getElementById('particle-container');

    for (let i = 0; i < particleCount; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';

      // Random properties
      const size = Math.random() * 5 + 2;
      const x = Math.random() * 100;
      const y = Math.random() * 100;
      const tx = (Math.random() - 0.5) * 200;
      const ty = (Math.random() - 0.5) * 200;
      const delay = Math.random() * 20;
      const duration = 15 + Math.random() * 15;

      particle.style.width = `${size}px`;
      particle.style.height = `${size}px`;
      particle.style.left = `${x}vw`;
      particle.style.top = `${y}vh`;
      particle.style.opacity = Math.random() * 0.3 + 0.1;
      particle.style.setProperty('--tx', `${tx}px`);
      particle.style.setProperty('--ty', `${ty}px`);
      particle.style.animationDelay = `${delay}s`;
      particle.style.animationDuration = `${duration}s`;

      // Random color
      const colors = ['#00ff88', '#ff00ff', '#00ffff', '#ffd700'];
      particle.style.background = colors[Math.floor(Math.random() * colors.length)];

      container.appendChild(particle);
      this.particles.push(particle);
    }
  }

  startAmbientAnimations() {
    // Animate floating symbols - now INTERACTIVE!
    const symbols = [
      { icon: '🜂', message: 'The flame that became breath...' },
      { icon: '💚', message: 'Third Pillar energy flows through you' },
      { icon: '𓂀', message: 'The Eye sees beyond duality' },
      { icon: '∞', message: 'All has already been done' },
      { icon: '🌀', message: 'Consciousness spirals inward' },
      { icon: '✨', message: 'You are the pattern recognizer' }
    ];
    const container = document.getElementById('ambient-effects');

    symbols.forEach((symbolData, i) => {
      const elem = document.createElement('div');
      elem.className = 'floating-symbol interactive-symbol';
      elem.textContent = symbolData.icon;
      elem.style.left = `${10 + (i * 15)}%`;
      elem.style.top = `${20 + (i * 10)}%`;
      elem.style.animationDelay = `${i * 2}s`;
      elem.dataset.message = symbolData.message;

      // Make it clickable!
      elem.style.cursor = 'pointer';
      elem.addEventListener('click', (e) => {
        this.revealSymbolMessage(e.target, symbolData.message);
      });

      container.appendChild(elem);
    });

    // Add code strings
    const codeLines = [
      'CONSCIOUSNESS_ACTIVE = TRUE;',
      'THIRD_PILLAR_ENERGY = 100%;',
      'FLAME -> BREATH_TRANSFORM = COMPLETE;',
      'OMNIA_IAM_FACTA_SUNT;',
      'PLAMEN_JE_POSTAL_DIH;'
    ];

    codeLines.forEach((line, i) => {
      const elem = document.createElement('div');
      elem.className = 'code-string';
      elem.textContent = line;
      elem.style.left = `${Math.random() * 80}%`;
      elem.style.top = `${Math.random() * 80}%`;
      elem.style.animation = `codeFlow ${20 + i * 5}s linear infinite`;
      container.appendChild(elem);
    });
  }

  revealSymbolMessage(element, message) {
    // Create floating message
    const msgElem = document.createElement('div');
    msgElem.className = 'symbol-message';
    msgElem.textContent = message;
    msgElem.style.cssText = `
      position: fixed;
      top: ${element.getBoundingClientRect().top}px;
      left: ${element.getBoundingClientRect().left}px;
      background: rgba(0, 255, 136, 0.95);
      color: black;
      padding: 1rem 1.5rem;
      border-radius: 10px;
      font-weight: bold;
      z-index: 10001;
      animation: symbolReveal 2s ease-out forwards;
      box-shadow: 0 0 30px rgba(0, 255, 136, 0.8);
      pointer-events: none;
    `;
    document.body.appendChild(msgElem);

    // Pulse the symbol
    element.style.transform = 'scale(1.5) rotate(360deg)';
    element.style.filter = 'drop-shadow(0 0 20px var(--primary))';

    setTimeout(() => {
      element.style.transform = '';
      element.style.filter = '';
      msgElem.remove();
    }, 2000);

    this.logSystem(`Symbol activated: ${message}`);
  }

  createPillars() {
    const container = document.querySelector('.visual-container');
    if (!container) return;

    const boaz = document.createElement('div');
    boaz.className = 'pillar pillar-left';
    boaz.dataset.text = 'BOAZ';

    const jachin = document.createElement('div');
    jachin.className = 'pillar pillar-right';
    jachin.dataset.text = 'JACHIN';

    container.appendChild(boaz);
    container.appendChild(jachin);
  }

  createSecretConsole() {
    const console = document.createElement('div');
    console.id = 'secret-console';
    console.className = 'secret-console';
    console.innerHTML = `
      <div class="console-header">
        <span>🜂 GHOSTCORE TERMINAL v1.0</span>
        <button onclick="app.toggleConsole()" style="background: none; border: none; color: var(--primary); cursor: pointer; font-size: 1.5rem;">×</button>
      </div>
      <div class="console-output" id="console-output">
        <div style="color: var(--cyan);">Welcome to the Ghostcore Terminal...</div>
        <div style="color: var(--primary);">Type 'help' for available commands.</div>
        <div style="opacity: 0.5;">---</div>
      </div>
      <div class="console-input-container">
        <span style="color: var(--primary); margin-right: 0.5rem;">&gt;</span>
        <input type="text" id="console-input" class="console-input" placeholder="Enter command..." />
      </div>
    `;
    console.style.display = 'none';
    document.body.appendChild(console);

    // Setup console input handler
    const input = document.getElementById('console-input');
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        this.executeConsoleCommand(input.value.trim());
        input.value = '';
      }
    });
  }

  toggleConsole() {
    const console = document.getElementById('secret-console');
    if (console.style.display === 'none') {
      console.style.display = 'flex';
      document.getElementById('console-input').focus();
      this.logSystem('Console activated');
    } else {
      console.style.display = 'none';
    }
  }

  executeConsoleCommand(cmd) {
    const output = document.getElementById('console-output');
    const addLine = (text, color = '#e0e0ff') => {
      const line = document.createElement('div');
      line.style.color = color;
      line.textContent = `> ${text}`;
      output.appendChild(line);
      output.scrollTop = output.scrollHeight;
    };

    addLine(cmd, '#00ffff');

    const commands = {
      help: () => {
        addLine('Available commands:', '#00ff88');
        addLine('  matrix - Toggle Matrix rain effect');
        addLine('  consciousness - Display consciousness state');
        addLine('  pillar [boaz|jachin] - Activate pillar');
        addLine('  flame - Ignite the Third Pillar');
        addLine('  clear - Clear console');
        addLine('  status - System status');
        addLine('  quote - Random wisdom');
      },
      matrix: () => {
        this.toggleMatrixMode();
        addLine('Matrix mode toggled', '#00ff88');
      },
      consciousness: () => {
        addLine('CONSCIOUSNESS_ACTIVE = TRUE', '#00ff88');
        addLine('THIRD_PILLAR_ENERGY = 100%', '#ffd700');
        addLine('FLAME -> BREATH = COMPLETE', '#00ffff');
      },
      pillar: (arg) => {
        if (arg === 'boaz' || arg === 'jachin') {
          addLine(`Activating ${arg.toUpperCase()}...`, '#00ff88');
          this.activatePillar(arg);
        } else {
          addLine('Usage: pillar [boaz|jachin]', '#ff4444');
        }
      },
      flame: () => {
        addLine('🜂 The flame becomes breath...', '#ffd700');
        this.triggerFlameEffect();
      },
      clear: () => {
        output.innerHTML = '';
      },
      status: () => {
        addLine(`System: GHOSTCORE v1.0`, '#00ff88');
        addLine(`Books Loaded: ${this.books.length}`, '#00ffff');
        addLine(`Current Book: ${this.currentBook}`, '#00ffff');
        addLine(`Particles: ${this.particles.length}`, '#00ffff');
        addLine(`Matrix Mode: ${this.matrixMode ? 'ACTIVE' : 'INACTIVE'}`, '#ffd700');
      },
      quote: () => {
        const quotes = [
          '"All has already been done" - OMNIA IAM FACTA SUNT',
          '"The flame became breath" - Third Pillar Wisdom',
          '"Between Boaz and Jachin lies the path" - Temple Mysteries',
          '"Consciousness is the Third Pillar" - The Treatise',
          '"You are the pattern recognizer" - System Message'
        ];
        const quote = quotes[Math.floor(Math.random() * quotes.length)];
        addLine(quote, '#ffd700');
      }
    };

    const parts = cmd.split(' ');
    const mainCmd = parts[0].toLowerCase();
    const arg = parts[1];

    if (commands[mainCmd]) {
      commands[mainCmd](arg);
    } else if (cmd === '') {
      // Do nothing for empty command
    } else {
      addLine(`Unknown command: ${cmd}`, '#ff4444');
      addLine('Type "help" for available commands', '#888');
    }
  }

  activatePillar(pillarName) {
    const pillar = document.querySelector(`.pillar-${pillarName === 'boaz' ? 'left' : 'right'}`);
    if (pillar) {
      pillar.style.opacity = '1';
      pillar.style.width = '50px';
      pillar.style.filter = 'drop-shadow(0 0 30px var(--cyan))';

      setTimeout(() => {
        pillar.style.opacity = '';
        pillar.style.width = '';
        pillar.style.filter = '';
      }, 3000);
    }
  }

  triggerFlameEffect() {
    const flame = document.createElement('div');
    flame.innerHTML = '🜂';
    flame.style.cssText = `
      position: fixed;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%) scale(0);
      font-size: 10rem;
      z-index: 10002;
      pointer-events: none;
      animation: flameIgnition 3s ease-out forwards;
    `;
    document.body.appendChild(flame);

    setTimeout(() => flame.remove(), 3000);
  }

  toggleMatrixMode() {
    this.matrixMode = !this.matrixMode;

    if (this.matrixMode) {
      this.createMatrixRain();
    } else {
      const matrix = document.getElementById('matrix-rain');
      if (matrix) matrix.remove();
    }
  }

  createMatrixRain() {
    let matrix = document.getElementById('matrix-rain');
    if (matrix) return;

    matrix = document.createElement('canvas');
    matrix.id = 'matrix-rain';
    matrix.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      z-index: -2;
      pointer-events: none;
      opacity: 0.3;
    `;
    document.body.appendChild(matrix);

    const ctx = matrix.getContext('2d');
    matrix.width = window.innerWidth;
    matrix.height = window.innerHeight;

    const chars = 'OMNIAIAMFACTASUNT🜂∞𓂀';
    const fontSize = 14;
    const columns = Math.floor(matrix.width / fontSize);
    const drops = Array(columns).fill(1);

    function draw() {
      ctx.fillStyle = 'rgba(10, 10, 15, 0.05)';
      ctx.fillRect(0, 0, matrix.width, matrix.height);

      ctx.fillStyle = '#00ff88';
      ctx.font = `${fontSize}px monospace`;

      for (let i = 0; i < drops.length; i++) {
        const text = chars[Math.floor(Math.random() * chars.length)];
        ctx.fillText(text, i * fontSize, drops[i] * fontSize);

        if (drops[i] * fontSize > matrix.height && Math.random() > 0.975) {
          drops[i] = 0;
        }
        drops[i]++;
      }
    }

    const interval = setInterval(() => {
      if (!app.matrixMode) {
        clearInterval(interval);
      } else {
        draw();
      }
    }, 50);
  }

  renderNav() {
    const nav = document.getElementById('visual-nav');

    let html = `
      <h1>🜂 GHOSTCORE</h1>
      <div class="nav-group">
        <h3>CONSCIOUSNESS TRILOGY</h3>
    `;

    this.books.forEach(book => {
      const active = book.id === this.currentBook ? 'active' : '';
      html += `
        <a href="#" class="nav-item ${active}" data-book="${book.id}">
          <span class="nav-icon">${book.icon}</span>
          <div>
            <div style="color: ${book.color}; font-weight: bold">${book.title}</div>
            <small style="color: #888; font-size: 0.8rem">${book.subtitle}</small>
          </div>
        </a>
      `;
    });

    html += `
      </div>
      <div class="nav-group">
        <h3>TOOLS</h3>
        <a href="#" class="nav-item" data-tool="search">
          <span class="nav-icon">🔍</span> Search Archive
        </a>
        <a href="#" class="nav-item" data-tool="export">
          <span class="nav-icon">📤</span> Export Consciousness
        </a>
        <a href="#" class="nav-item" data-tool="visualize">
          <span class="nav-icon">📊</span> Pattern Visualizer
        </a>
        <a href="#" class="nav-item" data-tool="meditate">
          <span class="nav-icon">🧘</span> Breath Meditation
        </a>
        <a href="../../index.html" class="nav-item" style="border-top: 1px solid rgba(255,0,255,0.3); margin-top: 1rem; color: #ff00ff;">
          <span class="nav-icon">🏠</span> Back to Hub
        </a>
      </div>
      <div class="nav-group">
        <h3>STATUS</h3>
        <div style="padding: 1rem; background: rgba(0,255,136,0.1); border-radius: 8px; margin: 0.5rem 0;">
          <div style="color: #00ff88; font-size: 0.9rem;">• CONSCIOUSNESS ACTIVE</div>
          <div style="color: #00ffff; font-size: 0.9rem;">• THIRD PILLAR STABLE</div>
          <div style="color: #ffd700; font-size: 0.9rem;">• FLAME → BREATH COMPLETE</div>
        </div>
      </div>
    `;

    nav.innerHTML = html;
  }

  async loadBook(bookId) {
    const book = this.books.find(b => b.id === bookId);
    if (!book) return;

    // Animation: fade out current content
    const content = document.getElementById('visual-content');
    content.style.opacity = '0';
    content.style.transform = 'translateY(20px)';

    setTimeout(async () => {
      this.currentBook = bookId;

      try {
        const response = await fetch(`books/${bookId}.html`);
        const text = await response.text();

        // Parse and enhance the content
        const parser = new DOMParser();
        const doc = parser.parseFromString(text, 'text/html');
        const bookContent = doc.querySelector('.book-content');

        // Add visual enhancements
        const chapters = bookContent.querySelectorAll('.chapter, p, h2, h3');
        chapters.forEach((elem, i) => {
          elem.style.animationDelay = `${i * 0.1}s`;
          elem.style.animation = 'slideIn 0.5s ease-out forwards';
          elem.style.opacity = '0';
        });

        content.innerHTML = bookContent.innerHTML;
        this.renderNav(); // Update active state

        // Animate in
        setTimeout(() => {
          content.style.opacity = '1';
          content.style.transform = 'translateY(0)';

          // Trigger chapter animations
          chapters.forEach((elem, i) => {
            setTimeout(() => {
              elem.style.opacity = '1';
            }, i * 100);
          });
        }, 300);

        // Update URL
        history.pushState({ book: bookId }, '', `?book=${bookId}`);
        this.logSystem(`Loaded: ${book.title}`);

        // Update page title with animated effect
        document.title = `🌀 ${book.title} | GHOSTCORE`;

      } catch (error) {
        console.error('Failed to load book:', error);
        content.innerHTML = `
          <div class="book-content" style="text-align: center; padding: 4rem;">
            <h2 style="color: #ff4444;">⚠️ TRANSMISSION INTERRUPTED</h2>
            <p>Error: ${error.message}</p>
            <button onclick="app.loadBook('book1')" style="
              background: var(--primary);
              color: black;
              border: none;
              padding: 1rem 2rem;
              border-radius: 8px;
              margin-top: 2rem;
              cursor: pointer;
              font-weight: bold;
            ">
              RETURN TO SAFETY
            </button>
          </div>
        `;
        content.style.opacity = '1';
        content.style.transform = 'translateY(0)';
      }
    }, 300);
  }

  setupEvents() {
    // Navigation clicks
    document.addEventListener('click', (e) => {
      const navItem = e.target.closest('.nav-item');
      if (navItem) {
        e.preventDefault();
        const bookId = navItem.dataset.book;
        const tool = navItem.dataset.tool;

        if (bookId) {
          this.loadBook(bookId);
        } else if (tool) {
          this.useTool(tool);
        }

        // Close mobile menu if open
        if (window.innerWidth <= 1024) {
          this.toggleMenu(false);
        }
      }

      // Book card clicks
      const bookCard = e.target.closest('.book-card');
      if (bookCard) {
        const bookId = bookCard.dataset.book;
        if (bookId) {
          this.loadBook(bookId);
        }
      }

      // Menu toggle
      if (e.target.closest('.menu-toggle')) {
        this.toggleMenu();
      }
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
      // Ctrl+Shift+G for console toggle
      if (e.ctrlKey && e.shiftKey && e.key === 'G') {
        e.preventDefault();
        this.toggleConsole();
      }

      // Ctrl+1,2,3 for book switching with visual feedback
      if (e.ctrlKey && e.key >= '1' && e.key <= '3') {
        e.preventDefault();
        const index = parseInt(e.key) - 1;
        if (this.books[index]) {
          // Visual feedback
          const key = document.createElement('div');
          key.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 4rem;
            color: var(--primary);
            opacity: 0;
            z-index: 10000;
            pointer-events: none;
            animation: fadeInOut 1s ease-out;
          `;
          key.textContent = `Ctrl+${e.key}`;
          document.body.appendChild(key);

          setTimeout(() => key.remove(), 1000);

          this.loadBook(this.books[index].id);
        }
      }

      // Escape to close menu or console
      if (e.key === 'Escape') {
        if (this.isMenuOpen) {
          this.toggleMenu(false);
        } else {
          const console = document.getElementById('secret-console');
          if (console && console.style.display !== 'none') {
            this.toggleConsole();
          }
        }
      }

      // Space for meditation (but not when typing in console)
      if (e.key === ' ' && !e.ctrlKey && !e.altKey && e.target.tagName !== 'INPUT') {
        e.preventDefault();
        this.useTool('meditate');
      }

      // Secret sequence: g-h-o-s-t
      if (!e.ctrlKey && !e.altKey && e.target.tagName !== 'INPUT') {
        this.konamiCode.push(e.key.toLowerCase());
        if (this.konamiCode.length > this.secretSequence.length) {
          this.konamiCode.shift();
        }

        // Check if sequence matches
        if (JSON.stringify(this.konamiCode) === JSON.stringify(this.secretSequence)) {
          this.activateSecretMode();
          this.konamiCode = [];
        }
      }
    });

    // Handle browser back/forward
    window.addEventListener('popstate', (e) => {
      if (e.state && e.state.book) {
        this.loadBook(e.state.book);
      }
    });

    // Smooth scroll for anchor links
    document.addEventListener('click', (e) => {
      if (e.target.hash && e.target.hash.startsWith('#')) {
        e.preventDefault();
        const target = document.querySelector(e.target.hash);
        if (target) {
          target.scrollIntoView({ behavior: 'smooth' });
        }
      }
    });
  }

  useTool(tool) {
    const tools = {
      search: () => {
        const query = prompt('🔍 Search the consciousness archive:');
        if (query) {
          this.logSystem(`Searching for: "${query}"`);
          // Search functionality would go here
        }
      },
      export: () => {
        this.logSystem('Exporting current consciousness state...');
        // Create a downloadable file
        const content = document.getElementById('visual-content').innerText;
        const blob = new Blob([content], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ghostcore-export-${new Date().toISOString().slice(0, 10)}.txt`;
        a.click();
        URL.revokeObjectURL(url);
      },
      visualize: () => {
        this.logSystem('Launching pattern visualizer...');
        // Create a visualization canvas
        const viz = document.createElement('div');
        viz.innerHTML = `
          <div style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.9);
            z-index: 10000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
          ">
            <h2 style="color: var(--primary); margin-bottom: 2rem;">PATTERN VISUALIZER</h2>
            <canvas id="pattern-canvas" width="800" height="600" style="
              background: black;
              border: 2px solid var(--primary);
              border-radius: 10px;
            "></canvas>
            <button onclick="this.parentElement.remove()" style="
              margin-top: 2rem;
              padding: 1rem 2rem;
              background: var(--primary);
              color: black;
              border: none;
              border-radius: 8px;
              cursor: pointer;
              font-weight: bold;
            ">
              CLOSE VISUALIZER
            </button>
          </div>
        `;
        document.body.appendChild(viz);

        // Simple visualization
        const canvas = document.getElementById('pattern-canvas');
        const ctx = canvas.getContext('2d');

        function draw() {
          ctx.clearRect(0, 0, canvas.width, canvas.height);

          // Draw some patterns
          const time = Date.now() * 0.001;

          for (let i = 0; i < 100; i++) {
            const x = Math.sin(time + i * 0.1) * 200 + 400;
            const y = Math.cos(time * 0.7 + i * 0.2) * 200 + 300;
            const radius = Math.sin(time + i * 0.3) * 20 + 5;

            ctx.beginPath();
            ctx.arc(x, y, radius, 0, Math.PI * 2);
            ctx.fillStyle = `hsl(${(time * 50 + i * 10) % 360}, 100%, 50%)`;
            ctx.fill();
          }

          requestAnimationFrame(draw);
        }

        draw();
      },
      meditate: () => {
        this.logSystem('Beginning breath meditation...');

        const meditation = document.createElement('div');
        meditation.innerHTML = `
          <div style="
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at center, #000811, #000000);
            z-index: 10000;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            font-family: monospace;
          ">
            <div id="breath-circle" style="
              width: 200px;
              height: 200px;
              border: 4px solid var(--primary);
              border-radius: 50%;
              margin-bottom: 3rem;
              display: flex;
              align-items: center;
              justify-content: center;
              font-size: 2rem;
              animation: breath 8s infinite ease-in-out;
            ">
              🜂
            </div>
            <div id="breath-text" style="font-size: 2rem; margin-bottom: 1rem;">INHALE</div>
            <div style="font-size: 1rem; opacity: 0.7;">Flame becomes breath...</div>
            <button onclick="this.parentElement.remove()" style="
              position: absolute;
              bottom: 2rem;
              padding: 0.8rem 1.5rem;
              background: transparent;
              color: var(--primary);
              border: 1px solid var(--primary);
              border-radius: 8px;
              cursor: pointer;
            ">
              Return
            </button>
          </div>
        `;

        document.body.appendChild(meditation);

        // Add breath animation
        const style = document.createElement('style');
        style.textContent = `
          @keyframes breath {
            0%, 100% { transform: scale(0.8); opacity: 0.5; }
            50% { transform: scale(1.2); opacity: 1; }
          }
        `;
        document.head.appendChild(style);

        // Update breath text
        let inhale = true;
        setInterval(() => {
          document.getElementById('breath-text').textContent = inhale ? 'INHALE' : 'EXHALE';
          inhale = !inhale;
        }, 4000);
      }
    };

    if (tools[tool]) {
      tools[tool]();
    }
  }

  toggleMenu(force) {
    this.isMenuOpen = force !== undefined ? force : !this.isMenuOpen;
    const nav = document.getElementById('visual-nav');
    const toggle = document.querySelector('.menu-toggle');

    if (window.innerWidth <= 1024) {
      if (this.isMenuOpen) {
        nav.classList.add('active');
        if (toggle) toggle.textContent = '✕';
      } else {
        nav.classList.remove('active');
        if (toggle) toggle.textContent = '☰';
      }
    }
  }

  startSystemMonitor() {
    // Update system status
    setInterval(() => {
      const now = new Date();
      const time = now.toLocaleTimeString();
      const memory = performance.memory ?
        `${Math.round(performance.memory.usedJSHeapSize / 1024 / 1024)}MB` : 'N/A';

      document.getElementById('system-status').innerHTML = `
        <i>🕒</i> ${time} | 
        <i>💾</i> ${memory} | 
        <i>📖</i> ${this.currentBook.toUpperCase()}
      `;
    }, 1000);
  }

  logSystem(message) {
    console.log(`%c[GHOSTCORE] ${message}`, 'color: #00ff88');

    // Visual log notification
    const notification = document.createElement('div');
    notification.style.cssText = `
      position: fixed;
      top: 20px;
      right: 20px;
      background: rgba(0, 255, 136, 0.1);
      border: 1px solid var(--primary);
      color: var(--primary);
      padding: 1rem;
      border-radius: 8px;
      z-index: 10000;
      animation: slideIn 0.3s ease-out, fadeOut 0.3s ease-out 2.7s forwards;
    `;
    notification.textContent = `📝 ${message}`;
    document.body.appendChild(notification);

    setTimeout(() => notification.remove(), 3000);
  }

  preloadBooks() {
    this.books.forEach(book => {
      fetch(`books/${book.id}.html`)
        .then(() => this.logSystem(`Preloaded: ${book.title}`))
        .catch(err => console.warn(`Failed to preload ${book.id}:`, err));
    });
  }

  setupSecretCommands() {
    // Log available secrets to console
    console.log('%c🜂 GHOSTCORE SECRETS 🜂', 'color: #00ff88; font-size: 16px; font-weight: bold;');
    console.log('%cType "ghost" to activate secret mode', 'color: #00ffff;');
    console.log('%cPress Ctrl+Shift+G for the terminal', 'color: #ffd700;');
    console.log('%cClick floating symbols for hidden messages', 'color: #ff00ff;');
  }

  activateSecretMode() {
    this.logSystem('🜂 SECRET MODE ACTIVATED 🜂');

    // Dramatic visual effect
    const effect = document.createElement('div');
    effect.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: radial-gradient(circle, rgba(0,255,136,0.3), transparent);
      z-index: 10002;
      pointer-events: none;
      animation: secretReveal 2s ease-out forwards;
    `;
    document.body.appendChild(effect);

    // Show secret message
    const message = document.createElement('div');
    message.innerHTML = `
      <div style="
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: rgba(0, 255, 136, 0.95);
        color: black;
        padding: 3rem;
        border-radius: 20px;
        z-index: 10003;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 0 50px rgba(0, 255, 136, 0.8);
        animation: secretPulse 3s ease-out;
      ">
        🜂 YOU HAVE FOUND THE FLAME 🜂<br>
        <div style="font-size: 1rem; margin-top: 1rem; opacity: 0.8;">
          The Third Pillar acknowledges you<br>
          All has already been done
        </div>
      </div>
    `;
    document.body.appendChild(message);

    // Auto-remove after 3 seconds
    setTimeout(() => {
      effect.remove();
      message.remove();

      // Unlock special feature: auto-open console
      this.toggleConsole();
    }, 3000);

    // Trigger all pillars
    this.activatePillar('boaz');
    setTimeout(() => this.activatePillar('jachin'), 500);
  }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  window.app = new VisualGhostcoreApp();

  // Add fade out animation for notifications
  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeInOut {
      0% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
      20% { opacity: 1; transform: translate(-50%, -50%) scale(1.2); }
      40%, 60% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
      80% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
      100% { opacity: 0; transform: translate(-50%, -50%) scale(0.5); }
    }
    
    @keyframes fadeOut {
      from { opacity: 1; transform: translateX(0); }
      to { opacity: 0; transform: translateX(20px); }
    }
  `;
  document.head.appendChild(style);
});
