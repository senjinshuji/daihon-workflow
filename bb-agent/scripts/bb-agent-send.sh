#!/bin/bash

# BB-Agent Communication Script
# Handles inter-agent communication and logging

# Log file location
LOG_FILE="${BB_AGENT_HOME:-$(dirname "$0")/..}/logs/send_log.txt"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# Function to send message to another agent
send_message() {
    local target_agent="$1"
    local message="$2"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    
    # Log the message
    echo "[$timestamp] FROM: $CURRENT_AGENT TO: $target_agent" >> "$LOG_FILE"
    echo "MESSAGE: $message" >> "$LOG_FILE"
    echo "---" >> "$LOG_FILE"
    
    # Send to tmux session if exists
    if tmux has-session -t "$target_agent" 2>/dev/null; then
        tmux send-keys -t "$target_agent" "$message" Enter
        echo "Message sent to $target_agent"
    else
        echo "Warning: Session $target_agent not found"
        return 1
    fi
}

# Function to broadcast message to all agents
broadcast_message() {
    local message="$1"
    local agents=("MD" "CD" "Writer1" "Writer2" "Writer3" "Persona1" "Persona2" "Persona3")
    
    for agent in "${agents[@]}"; do
        if [ "$agent" != "$CURRENT_AGENT" ]; then
            send_message "$agent" "$message"
        fi
    done
}

# Function to log activity
log_activity() {
    local activity="$1"
    local timestamp=$(date "+%Y-%m-%d %H:%M:%S")
    echo "[$timestamp] ACTIVITY: $CURRENT_AGENT - $activity" >> "$LOG_FILE"
}

# Main execution
if [ $# -lt 2 ]; then
    echo "Usage: $0 <target_agent|broadcast> <message>"
    echo "Example: $0 CD 'Task completed'"
    echo "Example: $0 broadcast 'System update'"
    exit 1
fi

# Set current agent from environment or default
CURRENT_AGENT="${CURRENT_AGENT:-Unknown}"

if [ "$1" = "broadcast" ]; then
    broadcast_message "$2"
else
    send_message "$1" "$2"
fi