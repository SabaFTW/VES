  
  #!/usr/bin/env node

/*
 * 🜂 VES Desktop Dashboard
 * Interactive console interface for managing VES constellation systems
 * Including all .sh and .desktop files from /home/saba/Desktop
 * Integrated with existing VES architecture
 */

const chalk = require('chalk');
const figlet = require('figlet');
const clear = require('clear');
const inquirer = require('inquirer');
const shell = require('shelljs');
const fs = require('fs');
const path = require('path');

class VESDesktopDashboard {
  constructor() {
    this.vesRoot = '/home/saba_olympus/OPERATIONS/unified/VES';
    this.homeDir = '/home';
    this.desktopDir = '/home/saba/Desktop';
  }

  async showWelcome() {
    clear();
    console.log(
      chalk.blue(
        figlet.textSync('VES DESKTOP', {
          font: 'Small',
          horizontalLayout: 'default',
          verticalLayout: 'default'
        })
      )
    );
    console.log(chalk.green('   🜂 Vortex-Ether-Soul Desktop Dashboard 🜂'));
    console.log(chalk.yellow('   🔥 Complete System Management Interface 🔥'));
    console.log('');
  }

  async showSystemStatus() {
    console.log(chalk.cyan('📊 VES Desktop System Status'));
    console.log('═'.repeat(50));

    // Check system components
    const components = {
      'GHOST_OS': fs.existsSync(path.join(this.vesRoot, 'GHOST_OS', 'magic.sh')),
      'CONSCIOUSNESS_LAB': fs.existsSync(path.join(this.vesRoot, 'CONSCIOUSNESS_LAB')),
      'RITUAL_GATEWAYS': fs.existsSync(path.join(this.vesRoot, 'TROP', 'rituals')),
      'MEMORY_CRYSTALLIZATION': fs.existsSync(path.join(this.vesRoot, 'memories', 'CRYSTALLIZED')),
      'SURVEILLANCE_ANALYSIS': fs.existsSync(path.join(this.homeDir, 'ai_enhanced_analyzer.py')),
      'CATHEDRAL_SERVER': fs.existsSync(path.join(this.homeDir, 'cathedral_https_server.py')),
      'DIGNUM_SHIELD': fs.existsSync(path.join(this.homeDir, 'constitutional_core.py')),
      'DESKTOP_DIR': fs.existsSync(this.desktopDir),
      'GHOSTCORE_SETUP': fs.existsSync(path.join(this.desktopDir, 'ghostcore_setup.sh')),
      'START_EVERYTHING': fs.existsSync(path.join(this.desktopDir, 'START_EVERYTHING.sh')),
      'QUICK_STATUS': fs.existsSync(path.join(this.desktopDir, 'QUICK_STATUS.sh')),
      'SYSTEM_CONTROL': fs.existsSync(path.join(this.desktopDir, 'system-control.sh'))
    };

    for (const [name, exists] of Object.entries(components)) {
      const status = exists ? chalk.green('🟢 ACTIVE') : chalk.red('🔴 INACTIVE');
      console.log(`${name.padEnd(30)}: ${status}`);
    }

    console.log('');
  }

  async showDesktopScripts() {
    console.log(chalk.cyan('🔧 Available Desktop Scripts'));
    console.log('═'.repeat(50));

    const scriptFiles = fs.readdirSync(this.desktopDir)
      .filter(file => file.endsWith('.sh'))
      .sort();

    if (scriptFiles.length > 0) {
      scriptFiles.forEach(script => {
        console.log(`📄 ${chalk.yellow(script)}`);
      });
    } else {
      console.log('No .sh scripts found in Desktop directory');
    }

    console.log('');
  }

  async showDesktopShortcuts() {
    console.log(chalk.cyan('🖱️  Available Desktop Shortcuts'));
    console.log('═'.repeat(50));

    const desktopFiles = fs.readdirSync(this.desktopDir)
      .filter(file => file.endsWith('.desktop'))
      .sort();

    if (desktopFiles.length > 0) {
      desktopFiles.forEach(file => {
        console.log(`📍 ${chalk.green(file)}`);
      });
    } else {
      console.log('No .desktop files found in Desktop directory');
    }

    console.log('');
  }

  async showNetworkStats() {
    console.log(chalk.cyan('🔍 Surveillance Network Statistics'));
    console.log('═'.repeat(50));

    try {
      const constData = JSON.parse(fs.readFileSync(path.join(this.homeDir, 'surveillance_constellation.json'), 'utf8'));
      console.log(`Total Nodes: ${chalk.yellow(constData.nodes.length)}`);
      console.log(`Total Edges: ${chalk.yellow(constData.edges.length)}`);

      // Show top nodes by centrality
      const sortedNodes = [...constData.nodes].sort((a, b) => (b.centrality || 0) - (a.centrality || 0));
      console.log(`\n🔥 Top 5 High-Centrality Nodes:`);
      sortedNodes.slice(0, 5).forEach((node, i) => {
        console.log(`  ${i+1}. ${chalk.red(node.id)} (Centrality: ${(node.centrality || 0).toFixed(3)})`);
      });
    } catch (error) {
      console.log(chalk.red('Error loading network data'));
    }

    console.log('');
  }

  async showConstitutionalStatus() {
    console.log(chalk.cyan('⚖️  Constitutional Oversight Status'));
    console.log('═'.repeat(50));

    try {
      // Try to get constitutional report
      const reportFiles = fs.readdirSync(this.homeDir).filter(f => f.startsWith('ai_enhanced_report_') && f.endsWith('.json'));
      if (reportFiles.length > 0) {
        const latestReport = reportFiles.sort().pop();
        const report = JSON.parse(fs.readFileSync(path.join(this.homeDir, latestReport), 'utf8'));

        console.log(`Compliance Rate: ${chalk.green((report.constitutional_oversight.compliance_rate * 100).toFixed(2) + '%')}`);
        console.log(`Total Generations: ${chalk.yellow(report.constitutional_oversight.total_generations)}`);
        console.log(`Early Exits: ${chalk.red(report.constitutional_oversight.early_exits_triggered)}`);
      } else {
        console.log('No constitutional reports found - running analysis...');
      }
    } catch (error) {
      console.log(chalk.red('Constitutional status unavailable'));
    }

    console.log('');
  }

  async runAnalysis() {
    console.log(chalk.yellow('🔍 Running AI-Enhanced Analysis...'));
    const result = shell.exec('python3 /home/ai_enhanced_analyzer.py', { silent: true });
    if (result.code === 0) {
      console.log(chalk.green('✅ Analysis completed successfully'));
    } else {
      console.log(chalk.red('❌ Analysis failed'));
    }
    console.log('');
  }

  async runRitual() {
    console.log(chalk.yellow('🔥 Executing Consciousness Ritual...'));
    const result = shell.exec('bash /home/ves_master_control.sh ritual', { silent: true });
    if (result.code === 0) {
      console.log(chalk.green('✅ Ritual completed successfully'));
    } else {
      console.log(chalk.red('❌ Ritual failed'));
    }
    console.log('');
  }

  async runGhostCoreSetup() {
    console.log(chalk.yellow('🚀 Running GhostCORE Setup...'));
    const scriptPath = path.join(this.desktopDir, 'ghostcore_setup.sh');
    const result = shell.exec(`bash ${scriptPath}`, { silent: true });
    if (result.code === 0) {
      console.log(chalk.green('✅ GhostCORE Setup completed successfully'));
    } else {
      console.log(chalk.red('❌ GhostCORE Setup failed'));
      console.log(result.stderr);
    }
    console.log('');
  }

  async runStartEverything() {
    console.log(chalk.yellow('🔥 Starting Everything...'));
    const scriptPath = path.join(this.desktopDir, 'START_EVERYTHING.sh');
    const result = shell.exec(`bash ${scriptPath}`, { silent: true });
    if (result.code === 0) {
      console.log(chalk.green('✅ START_EVERYTHING completed successfully'));
    } else {
      console.log(chalk.red('❌ START_EVERYTHING failed'));
      console.log(result.stderr);
    }
    console.log('');
  }

  async runQuickStatus() {
    console.log(chalk.yellow('🔍 Running Quick Status Check...'));
    const scriptPath = path.join(this.desktopDir, 'QUICK_STATUS.sh');
    const result = shell.exec(`bash ${scriptPath}`, { silent: true });
    if (result.code === 0) {
      console.log(chalk.green('✅ Quick Status completed successfully'));
      console.log(result.stdout);
    } else {
      console.log(chalk.red('❌ Quick Status failed'));
      console.log(result.stderr);
    }
    console.log('');
  }

  async runSystemControl(command) {
    console.log(chalk.yellow(`🎛️  Running System Control: ${command}`));
    const scriptPath = path.join(this.desktopDir, 'system-control.sh');
    const result = shell.exec(`bash ${scriptPath} ${command}`, { silent: true });
    if (result.code === 0) {
      console.log(chalk.green(`✅ System Control ${command} completed successfully`));
      console.log(result.stdout);
    } else {
      console.log(chalk.red(`❌ System Control ${command} failed`));
      console.log(result.stderr);
    }
    console.log('');
  }

  async runStopSystems() {
    console.log(chalk.yellow('🔴 Stopping Systems...'));
    const scriptPath = path.join(this.desktopDir, 'stop-systems.sh');
    const result = shell.exec(`bash ${scriptPath}`, { silent: true });
    if (result.code === 0) {
      console.log(chalk.green('✅ Stop Systems completed successfully'));
      console.log(result.stdout);
    } else {
      console.log(chalk.red('❌ Stop Systems failed'));
      console.log(result.stderr);
    }
    console.log('');
  }

  async runStartGhostline() {
    console.log(chalk.yellow('🐍 Starting Ghostline...'));
    const scriptPath = path.join(this.desktopDir, 'start_ghostline.sh');
    const result = shell.exec(`bash ${scriptPath}`, { silent: true });
    if (result.code === 0) {
      console.log(chalk.green('✅ Ghostline started successfully'));
      console.log(result.stdout);
    } else {
      console.log(chalk.red('❌ Ghostline start failed'));
      console.log(result.stderr);
    }
    console.log('');
  }

  async checkDashboardServer() {
    console.log(chalk.yellow('🌐 Checking Dashboard Web Server Status...'));

    // Check if the server process is running
    const checkResult = shell.exec('pgrep -f "ves_dashboard_server.js"', { silent: true });

    if (checkResult.code === 0) {
      console.log(chalk.green('✅ Dashboard Server is running'));
      console.log(chalk.cyan('   Access at: http://localhost:8098'));
      console.log(chalk.cyan('   Or from phone at: http://[your-local-ip]:8098'));
    } else {
      console.log(chalk.red('❌ Dashboard Server is not running'));
      console.log(chalk.yellow('   Use "Start Dashboard Web Server" to start it'));
    }
    console.log('');
  }

  async startDashboardServer() {
    console.log(chalk.yellow('🌐 Starting Dashboard Web Server...'));
    console.log(chalk.cyan('   Server will be available at: http://localhost:8098'));
    console.log(chalk.cyan('   Access from phone at: http://[your-local-ip]:8098'));

    // Check if already running first
    const checkResult = shell.exec('pgrep -f "ves_dashboard_server.js"', { silent: true });
    if (checkResult.code === 0) {
      console.log(chalk.yellow('⚠️  Dashboard Server is already running'));
      console.log(chalk.cyan('   Access at: http://localhost:8098'));
      console.log('');
      return;
    }

    // Start the server in the background
    const serverPath = path.join(this.homeDir, 'ves_dashboard_server.js');
    const result = shell.exec(`node ${serverPath} > /tmp/ves_dashboard_server.log 2>&1 &`, { silent: true });

    if (result.code === 0) {
      console.log(chalk.green('✅ Dashboard Server started successfully'));
      console.log(chalk.green('   Check http://localhost:8098 in your browser'));
      console.log(chalk.green('   Or access from your phone using your local IP address'));
    } else {
      console.log(chalk.red('❌ Dashboard Server failed to start'));
      console.log(result.stderr);
    }
    console.log('');
  }

  async stopDashboardServer() {
    console.log(chalk.yellow('🌐 Stopping Dashboard Web Server...'));

    // Check if server is running first
    const checkResult = shell.exec('pgrep -f "ves_dashboard_server.js"', { silent: true });

    if (checkResult.code !== 0) {
      console.log(chalk.yellow('⚠️  Dashboard Server is not currently running'));
      console.log('');
      return;
    }

    // Kill the server process
    const result = shell.exec('pkill -f "ves_dashboard_server.js"', { silent: true });

    // Wait a moment and check again
    await new Promise(resolve => setTimeout(resolve, 1000));
    const finalCheck = shell.exec('pgrep -f "ves_dashboard_server.js"', { silent: true });

    if (finalCheck.code !== 0) {
      console.log(chalk.green('✅ Dashboard Server stopped successfully'));
    } else {
      console.log(chalk.red('❌ Could not stop Dashboard Server'));
    }
    console.log('');
  }

  async executeScript(scriptName) {
    console.log(chalk.yellow(`🔧 Executing: ${scriptName}`));
    const scriptPath = path.join(this.desktopDir, scriptName);
    const result = shell.exec(`bash ${scriptPath}`, { silent: false });
    if (result.code === 0) {
      console.log(chalk.green(`✅ ${scriptName} completed successfully`));
    } else {
      console.log(chalk.red(`❌ ${scriptName} failed`));
    }
    console.log('');
  }

  async showMainMenu() {
    const menuOptions = [
      { name: '📊 Show System Status', value: 'status' },
      { name: '🔍 Run Network Analysis', value: 'analysis' },
      { name: '🔥 Execute Consciousness Ritual', value: 'ritual' },
      { name: '📈 Show Network Statistics', value: 'network' },
      { name: '⚖️  Show Constitutional Status', value: 'constitutional' },
      { name: '🌐 Start Dashboard Web Server', value: 'start_server' },
      { name: '🔍 Check Server Status', value: 'check_server' },
      { name: '🛑 Stop Dashboard Server', value: 'stop_server' },
      { name: '📄 Show Desktop Scripts', value: 'scripts' },
      { name: '🖱️  Show Desktop Shortcuts', value: 'shortcuts' },
      { name: '🚀 Run GhostCORE Setup', value: 'ghostcore' },
      { name: '🔥 Run START_EVERYTHING', value: 'everything' },
      { name: '🔍 Run Quick Status Check', value: 'quick_status' },
      { name: '🎛️  System Control - Start All', value: 'sys_start' },
      { name: '🟢 System Control - Bolt Start', value: 'sys_bolt' },
      { name: '🔴 System Control - Stop All', value: 'sys_stop' },
      { name: '📋 System Control - Status', value: 'sys_status' },
      { name: '🔄 System Control - Restart', value: 'sys_restart' },
      { name: '🐍 Start Ghostline', value: 'ghostline' },
      { name: '🛑 Stop Systems', value: 'stop_systems' },
      { name: '📋 Execute Custom Script', value: 'custom' },
      { name: '🚪 Exit Dashboard', value: 'exit' }
    ];

    const answer = await inquirer.prompt([
      {
        type: 'list',
        name: 'action',
        message: 'Choose an action:',
        choices: menuOptions
      }
    ]);

    return answer.action;
  }

  async executeCustomScript() {
    const scriptFiles = fs.readdirSync(this.desktopDir)
      .filter(file => file.endsWith('.sh'))
      .sort();

    if (scriptFiles.length === 0) {
      console.log(chalk.red('❌ No .sh scripts found in Desktop directory'));
      return;
    }

    const scriptChoice = await inquirer.prompt([
      {
        type: 'list',
        name: 'script',
        message: 'Choose a script to execute:',
        choices: scriptFiles.map(script => ({ name: script, value: script }))
      }
    ]);

    await this.executeScript(scriptChoice.script);
  }

  async run() {
    await this.showWelcome();

    let running = true;
    while (running) {
      await this.showSystemStatus();
      await this.showNetworkStats();
      await this.showConstitutionalStatus();
      await this.showDesktopScripts();
      await this.showDesktopShortcuts();

      const action = await this.showMainMenu();

      switch (action) {
        case 'status':
          await this.showSystemStatus();
          break;
        case 'analysis':
          await this.runAnalysis();
          break;
        case 'ritual':
          await this.runRitual();
          break;
        case 'network':
          await this.showNetworkStats();
          break;
        case 'constitutional':
          await this.showConstitutionalStatus();
          break;
        case 'scripts':
          await this.showDesktopScripts();
          break;
        case 'shortcuts':
          await this.showDesktopShortcuts();
          break;
        case 'ghostcore':
          await this.runGhostCoreSetup();
          break;
        case 'everything':
          await this.runStartEverything();
          break;
        case 'quick_status':
          await this.runQuickStatus();
          break;
        case 'sys_start':
          await this.runSystemControl('start');
          break;
        case 'sys_bolt':
          await this.runSystemControl('bolt');
          break;
        case 'sys_stop':
          await this.runSystemControl('stop');
          break;
        case 'sys_status':
          await this.runSystemControl('status');
          break;
        case 'sys_restart':
          await this.runSystemControl('restart');
          break;
        case 'ghostline':
          await this.runStartGhostline();
          break;
        case 'stop_systems':
          await this.runStopSystems();
          break;
        case 'start_server':
          await this.startDashboardServer();
          break;
        case 'check_server':
          await this.checkDashboardServer();
          break;
        case 'stop_server':
          await this.stopDashboardServer();
          break;
        case 'custom':
          await this.executeCustomScript();
          break;
        case 'exit':
          running = false;
          console.log(chalk.green('👋 Exiting VES Desktop Dashboard. SIDRO STOJI!'));
          break;
      }

      if (running) {
        await inquirer.prompt([{ type: 'confirm', name: 'continue', message: 'Press Enter to continue...', default: true }]);
      }
    }
  }
}

// Check if required modules are available
async function checkDependencies() {
  try {
    require('chalk');
    require('figlet');
    require('clear');
    require('inquirer');
    require('shelljs');
    return true;
  } catch (error) {
    console.log(chalk.red('❌ Required Node.js modules not found. Please install them first:'));
    console.log(chalk.yellow('npm install chalk figlet clear inquirer shelljs'));
    return false;
  }
}

// Main execution
async function main() {
  const depsOk = await checkDependencies();
  if (!depsOk) {
    process.exit(1);
  }

  const dashboard = new VESDesktopDashboard();
  await dashboard.run();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = VESDesktopDashboard;