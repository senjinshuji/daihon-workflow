#!/bin/bash

# Claude Code SDK Helper Script
# Common functions for workflow execution

# Execute Claude Code SDK with standard settings
run_claude_sdk() {
    local prompt="$1"
    local tools="${2:-Read,Write}"
    local max_turns="${3:-40}"
    
    npx @anthropic-ai/claude-code \
        --allowedTools "$tools" \
        --max-turns "$max_turns" \
        --verbose \
        --permission-mode "acceptEdits" \
        -p "$prompt"
}

# Load and process prompt template
load_prompt() {
    local prompt_file="$1"
    shift
    
    if [ ! -f "$prompt_file" ]; then
        echo "::error::Prompt file not found: $prompt_file"
        return 1
    fi
    
    local prompt=$(cat "$prompt_file")
    
    # Replace all provided placeholders
    while [ $# -gt 0 ]; do
        local key="$1"
        local value="$2"
        prompt="${prompt//$key/$value}"
        shift 2
    done
    
    echo "$prompt"
}

# Check output files
check_output() {
    local dir="$1"
    local pattern="${2:-*}"
    local min_count="${3:-1}"
    
    if [ ! -d "$dir" ]; then
        echo "::error::Directory not found: $dir"
        return 1
    fi
    
    local count=$(find "$dir" -name "$pattern" -type f | wc -l)
    
    if [ "$count" -lt "$min_count" ]; then
        echo "::error::Expected at least $min_count files, found $count"
        return 1
    fi
    
    echo "::notice::Found $count files matching $pattern"
    return 0
}

# Set GitHub output
set_output() {
    local key="$1"
    local value="$2"
    echo "${key}=${value}" >> $GITHUB_OUTPUT
}