# BB-Agent System

MD-based multi-agent creative script generation system following Claude Code Communications design.

## Quick Start

1. **Initialize agents:**
   ```bash
   cd bb-agent/scripts
   ./init-agents.sh
   ```

2. **Create new project:**
   ```bash
   ./start-project.sh new my_project data.csv
   ```

3. **Start workflow:**
   ```bash
   ./start-project.sh start my_project
   ```

## System Commands

### Agent Management
- `./init-agents.sh` - Initialize all 8 agents
- `./tmux-manager.sh list` - Show agent status
- `./tmux-manager.sh attach <agent>` - Connect to agent
- `./tmux-manager.sh dashboard` - View all agents

### Project Management
- `./start-project.sh new <name> <csv>` - Create project
- `./start-project.sh list` - List projects
- `./start-project.sh start <name>` - Start workflow
- `./start-project.sh status <name>` - Check progress

## Agent Roles

- **MD**: Marketing Director - Strategy & analysis
- **CD**: Creative Director - Quality control
- **Writer1-3**: Script creators (15 scripts total)
- **Persona1-3**: Evaluators (45 evaluations total)

## Workflow

1. MD analyzes CSV → creates strategy files
2. CD creates personality files for all agents
3. Writers produce 5 scripts each (15 total)
4. Personas evaluate all scripts (45 evaluations)
5. CD integrates analysis
6. Loop continues for improvement