#!/bin/bash

# BB-Agent Initialization Script
# Creates and initializes all 8 agent sessions

# Set BB_AGENT_HOME
export BB_AGENT_HOME="$(dirname "$0")/.."

# Agent list
AGENTS=("MD" "CD" "Writer1" "Writer2" "Writer3" "Persona1" "Persona2" "Persona3")

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Starting BB-Agent System Initialization...${NC}"

# Kill existing sessions if any
for agent in "${AGENTS[@]}"; do
    if tmux has-session -t "$agent" 2>/dev/null; then
        echo "Killing existing session: $agent"
        tmux kill-session -t "$agent"
    fi
done

# Create new sessions for each agent
for agent in "${AGENTS[@]}"; do
    echo -e "${GREEN}Creating session for $agent...${NC}"
    tmux new-session -d -s "$agent" -c "$BB_AGENT_HOME"
    
    # Set environment variable for agent identification
    tmux send-keys -t "$agent" "export CURRENT_AGENT=$agent" Enter
    tmux send-keys -t "$agent" "export BB_AGENT_HOME=$BB_AGENT_HOME" Enter
    tmux send-keys -t "$agent" "clear" Enter
    
    # Send initialization message
    tmux send-keys -t "$agent" "echo '=== $agent Agent Initialized ===' " Enter
    tmux send-keys -t "$agent" "echo 'Ready to receive instructions...'" Enter
    tmux send-keys -t "$agent" "echo ''" Enter
done

echo -e "${GREEN}All agents initialized successfully!${NC}"
echo ""
echo "To attach to an agent session:"
echo "  tmux attach -t <agent_name>"
echo ""
echo "Available agents: ${AGENTS[*]}"
echo ""
echo "To start the chain initialization:"
echo "  1. Attach to MD: tmux attach -t MD"
echo "  2. Type: あなたはMDです。指示書に従って"