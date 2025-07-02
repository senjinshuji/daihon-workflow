#!/bin/bash

# BB-Agent Tmux Session Manager
# Provides utilities for managing agent sessions

# Set BB_AGENT_HOME
export BB_AGENT_HOME="$(dirname "$0")/.."

# Agent list
AGENTS=("MD" "CD" "Writer1" "Writer2" "Writer3" "Persona1" "Persona2" "Persona3")

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to show all sessions
show_sessions() {
    echo -e "${BLUE}Active BB-Agent Sessions:${NC}"
    echo "=========================="
    for agent in "${AGENTS[@]}"; do
        if tmux has-session -t "$agent" 2>/dev/null; then
            echo -e "${GREEN}✓ $agent${NC} - Active"
        else
            echo -e "${RED}✗ $agent${NC} - Not running"
        fi
    done
    echo ""
}

# Function to attach to a session
attach_session() {
    local agent="$1"
    if tmux has-session -t "$agent" 2>/dev/null; then
        tmux attach -t "$agent"
    else
        echo -e "${RED}Error: Session $agent not found${NC}"
        exit 1
    fi
}

# Function to send command to agent
send_command() {
    local agent="$1"
    local command="$2"
    if tmux has-session -t "$agent" 2>/dev/null; then
        tmux send-keys -t "$agent" "$command" Enter
        echo -e "${GREEN}Command sent to $agent${NC}"
    else
        echo -e "${RED}Error: Session $agent not found${NC}"
        exit 1
    fi
}

# Function to view agent window
view_agent() {
    local agent="$1"
    if tmux has-session -t "$agent" 2>/dev/null; then
        tmux capture-pane -t "$agent" -p | tail -20
    else
        echo -e "${RED}Error: Session $agent not found${NC}"
        exit 1
    fi
}

# Function to kill all sessions
kill_all() {
    echo -e "${YELLOW}Stopping all BB-Agent sessions...${NC}"
    for agent in "${AGENTS[@]}"; do
        if tmux has-session -t "$agent" 2>/dev/null; then
            tmux kill-session -t "$agent"
            echo -e "${RED}Killed session: $agent${NC}"
        fi
    done
    echo -e "${GREEN}All sessions terminated${NC}"
}

# Function to create dashboard view
dashboard() {
    tmux new-session -d -s bb-dashboard
    
    # Create 8 panes for all agents
    tmux split-window -h -t bb-dashboard
    tmux split-window -v -t bb-dashboard:0.0
    tmux split-window -v -t bb-dashboard:0.1
    tmux split-window -h -t bb-dashboard:0.2
    tmux split-window -h -t bb-dashboard:0.3
    tmux split-window -v -t bb-dashboard:0.4
    tmux split-window -v -t bb-dashboard:0.5
    
    # Attach to each agent session in panes
    for i in {0..7}; do
        agent="${AGENTS[$i]}"
        if tmux has-session -t "$agent" 2>/dev/null; then
            tmux send-keys -t bb-dashboard:0.$i "tmux attach -t $agent" Enter
        fi
    done
    
    tmux attach -t bb-dashboard
}

# Main menu
case "$1" in
    "list"|"ls")
        show_sessions
        ;;
    "attach"|"a")
        if [ -z "$2" ]; then
            echo "Usage: $0 attach <agent_name>"
            exit 1
        fi
        attach_session "$2"
        ;;
    "send"|"s")
        if [ -z "$2" ] || [ -z "$3" ]; then
            echo "Usage: $0 send <agent_name> <command>"
            exit 1
        fi
        send_command "$2" "$3"
        ;;
    "view"|"v")
        if [ -z "$2" ]; then
            echo "Usage: $0 view <agent_name>"
            exit 1
        fi
        view_agent "$2"
        ;;
    "kill-all"|"ka")
        kill_all
        ;;
    "dashboard"|"d")
        dashboard
        ;;
    *)
        echo "BB-Agent Tmux Manager"
        echo "===================="
        echo ""
        echo "Commands:"
        echo "  list|ls              - Show all agent sessions"
        echo "  attach|a <agent>     - Attach to agent session"
        echo "  send|s <agent> <cmd> - Send command to agent"
        echo "  view|v <agent>       - View last 20 lines of agent"
        echo "  kill-all|ka          - Kill all agent sessions"
        echo "  dashboard|d          - Create split-pane dashboard"
        echo ""
        echo "Agents: ${AGENTS[*]}"
        ;;
esac