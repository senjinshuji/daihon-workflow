#!/bin/bash

# BB-Agent Project Starter
# Automates project initialization and workflow

# Set BB_AGENT_HOME
export BB_AGENT_HOME="$(dirname "$0")/.."
PROJECT_DIR="$BB_AGENT_HOME/projects"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to create new project
create_project() {
    local project_name="$1"
    local csv_file="$2"
    
    if [ -z "$project_name" ] || [ -z "$csv_file" ]; then
        echo "Usage: $0 new <project_name> <csv_file>"
        exit 1
    fi
    
    # Check if CSV file exists
    if [ ! -f "$csv_file" ]; then
        echo -e "${RED}Error: CSV file not found: $csv_file${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Creating new project: $project_name${NC}"
    
    # Create project directory structure
    local project_path="$PROJECT_DIR/$project_name"
    mkdir -p "$project_path"/{csv_data,md_strategy,loop1/{personalities,scripts,evaluations,analysis},loop2,loop3}
    
    # Copy CSV file
    cp "$csv_file" "$project_path/csv_data/"
    
    echo -e "${GREEN}Project created at: $project_path${NC}"
    echo ""
    echo "Next steps:"
    echo "1. Initialize agents: ./init-agents.sh"
    echo "2. Attach to MD: ./tmux-manager.sh attach MD"
    echo "3. Start project: プロジェクト名『$project_name』でCSVデータを分析してloop1を開始してください"
}

# Function to list projects
list_projects() {
    echo -e "${BLUE}Available Projects:${NC}"
    echo "==================="
    if [ -d "$PROJECT_DIR" ]; then
        for project in "$PROJECT_DIR"/*; do
            if [ -d "$project" ]; then
                basename "$project"
            fi
        done
    else
        echo "No projects found"
    fi
}

# Function to start workflow
start_workflow() {
    local project_name="$1"
    
    if [ -z "$project_name" ]; then
        echo "Usage: $0 start <project_name>"
        exit 1
    fi
    
    local project_path="$PROJECT_DIR/$project_name"
    
    if [ ! -d "$project_path" ]; then
        echo -e "${RED}Error: Project not found: $project_name${NC}"
        exit 1
    fi
    
    echo -e "${YELLOW}Starting workflow for project: $project_name${NC}"
    
    # Initialize agents if not already running
    if ! tmux has-session -t "MD" 2>/dev/null; then
        echo "Initializing agents..."
        "$BB_AGENT_HOME/scripts/init-agents.sh"
        sleep 2
    fi
    
    # Send start command to MD
    local start_command="プロジェクト名『$project_name』でCSVデータを分析してloop1を開始してください"
    tmux send-keys -t "MD" "$start_command" Enter
    
    echo -e "${GREEN}Workflow started!${NC}"
    echo ""
    echo "Monitor progress:"
    echo "  ./tmux-manager.sh list    - Show all agents"
    echo "  ./tmux-manager.sh attach MD - View MD agent"
    echo "  ./tmux-manager.sh dashboard - View all agents"
}

# Function to show project status
show_status() {
    local project_name="$1"
    
    if [ -z "$project_name" ]; then
        echo "Usage: $0 status <project_name>"
        exit 1
    fi
    
    local project_path="$PROJECT_DIR/$project_name"
    
    if [ ! -d "$project_path" ]; then
        echo -e "${RED}Error: Project not found: $project_name${NC}"
        exit 1
    fi
    
    echo -e "${BLUE}Project Status: $project_name${NC}"
    echo "================================"
    
    # Check for strategy files
    echo -e "\n${YELLOW}Strategy Files:${NC}"
    for file in product_analysis target_analysis copywriter_instructions persona_evaluation_criteria creative_strategy; do
        if [ -f "$project_path/md_strategy/$file.md" ]; then
            echo -e "${GREEN}✓ $file.md${NC}"
        else
            echo -e "${RED}✗ $file.md${NC}"
        fi
    done
    
    # Check loops
    for loop in loop1 loop2 loop3; do
        if [ -d "$project_path/$loop" ] && [ "$(ls -A "$project_path/$loop")" ]; then
            echo -e "\n${YELLOW}$loop Status:${NC}"
            
            # Count files
            local personalities=$(find "$project_path/$loop/personalities" -name "*.md" 2>/dev/null | wc -l)
            local scripts=$(find "$project_path/$loop/scripts" -name "*.md" 2>/dev/null | wc -l)
            local evaluations=$(find "$project_path/$loop/evaluations" -name "*.md" 2>/dev/null | wc -l)
            
            echo "  Personalities: $personalities files"
            echo "  Scripts: $scripts files"
            echo "  Evaluations: $evaluations files"
            
            if [ -f "$project_path/$loop/analysis/integrated_analysis_$loop.md" ]; then
                echo -e "  ${GREEN}✓ Integrated analysis complete${NC}"
            fi
        fi
    done
}

# Main menu
case "$1" in
    "new")
        create_project "$2" "$3"
        ;;
    "list"|"ls")
        list_projects
        ;;
    "start")
        start_workflow "$2"
        ;;
    "status")
        show_status "$2"
        ;;
    *)
        echo "BB-Agent Project Manager"
        echo "======================="
        echo ""
        echo "Commands:"
        echo "  new <name> <csv>  - Create new project"
        echo "  list|ls           - List all projects"
        echo "  start <name>      - Start project workflow"
        echo "  status <name>     - Show project status"
        echo ""
        echo "Example:"
        echo "  $0 new cosmetics_campaign data.csv"
        echo "  $0 start cosmetics_campaign"
        ;;
esac