#!/bin/bash

# A modular approach to project scaffolding
# Author: Anumeya Sehgal (KreativeThinker)
# Github: https://github.com/KreativeThinker/pinit

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STACKS_DIR="$SCRIPT_DIR/stacks"
TEMPLATES_DIR="$SCRIPT_DIR/templates"

# Global variables
PROJECT_NAME=""
PROJECT_DESCRIPTION=""
FRAMEWORK=""
ENABLE_FORMATTERS=false
INSTALL_PRECOMMITS=false
INIT_COMMITIZEN=false
CREATE_DOCKERFILE=false
CREATE_README=false
INIT_GIT=false
GIT_ORIGIN=""
GIT_BRANCH="main"

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_step() {
    echo -e "${PURPLE}🔧 $1${NC}"
}

# Check if required commands exist
check_dependencies() {
    local missing_deps=()
    
    # Always required
    if ! command -v git &> /dev/null; then
        missing_deps+=("git")
    fi
    
    # Framework specific checks will be done in stack scripts
    
    if [ ${#missing_deps[@]} -ne 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        exit 1
    fi
}

# List available stacks
list_stacks() {
    echo -e "${BLUE}Available stacks:${NC}"
    local i=1
    for stack in "$STACKS_DIR"/*.sh; do
        if [ -f "$stack" ]; then
            local stack_name=$(basename "$stack" .sh)
            echo "  $i. $stack_name"
            ((i++))
        fi
    done
}

# Get user input
get_user_input() {
    echo -e "${PURPLE}🚀 Project Setup Utility${NC}"
    echo "=================================="
    
    # Project name
    while [[ -z "$PROJECT_NAME" ]]; do
        read -p "📝 Project name: " PROJECT_NAME
        if [[ -z "$PROJECT_NAME" ]]; then
            log_error "Project name is required!"
        fi
    done
    
    # Project description
    read -p "📄 Project description: " PROJECT_DESCRIPTION
    
    # Framework selection
    echo
    list_stacks
    echo
    
    local stack_files=("$STACKS_DIR"/*.sh)
    local num_stacks=${#stack_files[@]}
    
    while true; do
        read -p "🔧 Select framework (1-$num_stacks): " choice
        if [[ "$choice" =~ ^[0-9]+$ ]] && [ "$choice" -ge 1 ] && [ "$choice" -le "$num_stacks" ]; then
            FRAMEWORK=$(basename "${stack_files[$((choice-1))]}" .sh)
            break
        else
            log_error "Please enter a number between 1 and $num_stacks"
        fi
    done
    
    # Boolean options
    read -p "🎨 Enable formatters? (Y/n): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Nn]$ ]] && ENABLE_FORMATTERS=true
    
    read -p "🔒 Install pre-commit hooks? (Y/n): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Nn]$ ]] && INSTALL_PRECOMMITS=true
    
    read -p "📝 Initialize commitizen? (Y/n): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Nn]$ ]] && INIT_COMMITIZEN=true
    
    read -p "🐳 Create Dockerfile? (Y/n): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Nn]$ ]] && CREATE_DOCKERFILE=true
    
    read -p "📄 Create README? (Y/n): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Nn]$ ]] && CREATE_README=true
    
    read -p "🔧 Initialize git? (Y/n): " -n 1 -r
    echo
    [[ ! $REPLY =~ ^[Nn]$ ]] && INIT_GIT=true
    
    if [ "$INIT_GIT" = true ]; then
        read -p "🌐 Git origin URL (optional): " GIT_ORIGIN
        read -p "🌿 Git branch name (main): " input_branch
        [[ -n "$input_branch" ]] && GIT_BRANCH="$input_branch"
    fi
}

# Export variables for use in stack scripts
export_variables() {
    export PROJECT_NAME
    export PROJECT_DESCRIPTION
    export FRAMEWORK
    export ENABLE_FORMATTERS
    export INSTALL_PRECOMMITS
    export INIT_COMMITIZEN
    export CREATE_DOCKERFILE
    export CREATE_README
    export INIT_GIT
    export GIT_ORIGIN
    export GIT_BRANCH
    export TEMPLATES_DIR
    export SCRIPT_DIR
}

# Copy template files
copy_template() {
    local template_path="$1"
    local dest_path="$2"
    local template_vars="$3"
    
    if [ -f "$TEMPLATES_DIR/$template_path" ]; then
        if [ -n "$template_vars" ]; then
            # Process template variables
            envsubst "$template_vars" < "$TEMPLATES_DIR/$template_path" > "$dest_path"
        else
            cp "$TEMPLATES_DIR/$template_path" "$dest_path"
        fi
        log_success "Created $dest_path"
    else
        log_warning "Template $template_path not found"
    fi
}

# Setup formatters
setup_formatters() {
    [ "$ENABLE_FORMATTERS" != true ] && return
    
    log_step "Setting up formatters..."
    
    # Copy prettier config if it exists
    if [ -f "$TEMPLATES_DIR/prettier/.prettierrc" ]; then
        cp "$TEMPLATES_DIR/prettier/.prettierrc" .
        log_success "Copied prettier config"
    fi
    
    # Copy other formatter configs based on framework
    if [[ "$FRAMEWORK" == *"python"* ]] || [[ "$FRAMEWORK" == "django" ]] || [[ "$FRAMEWORK" == "fastapi" ]]; then
        # Python formatting configs are typically in pyproject.toml
        log_info "Python formatting configs will be in pyproject.toml"
    fi
}

# Setup pre-commit hooks
setup_precommits() {
    [ "$INSTALL_PRECOMMITS" != true ] && return
    
    log_step "Setting up pre-commit hooks..."
    
    # Determine which pre-commit config to use
    local precommit_config=""
    if [[ "$FRAMEWORK" == *"python"* ]] || [[ "$FRAMEWORK" == "django" ]] || [[ "$FRAMEWORK" == "fastapi" ]]; then
        precommit_config="python.yaml"
    else
        precommit_config="js.yaml"
    fi
    
    if [ -f "$TEMPLATES_DIR/pre-commit/$precommit_config" ]; then
        cp "$TEMPLATES_DIR/pre-commit/$precommit_config" .pre-commit-config.yaml
        log_success "Copied pre-commit config"
        
        # Install pre-commit hooks
        if command -v pre-commit &> /dev/null; then
            pre-commit install
            log_success "Installed pre-commit hooks"
        else
            log_warning "pre-commit command not found. Install it manually later."
        fi
    else
        log_warning "Pre-commit config $precommit_config not found"
    fi
}

# Setup commitizen
setup_commitizen() {
    [ "$INIT_COMMITIZEN" != true ] && return
    
    log_step "Setting up commitizen..."
    
    # Framework-specific commitizen setup will be handled in stack scripts
    log_info "Commitizen setup delegated to stack script"
}

# Create Dockerfile
create_dockerfile() {
    [ "$CREATE_DOCKERFILE" != true ] && return
    
    log_step "Creating Dockerfile..."
    
    # Determine which Dockerfile to use
    local dockerfile_template=""
    if [[ "$FRAMEWORK" == "fastapi" ]]; then
        dockerfile_template="fastapi"
    elif [[ "$FRAMEWORK" == "django" ]] || [[ "$FRAMEWORK" == *"python"* ]]; then
        dockerfile_template="python"
    elif [[ "$FRAMEWORK" == "next" ]] || [[ "$FRAMEWORK" == "reactvite" ]]; then
        dockerfile_template="node"
    fi
    
    if [ -n "$dockerfile_template" ] && [ -f "$TEMPLATES_DIR/docker/Dockerfile.$dockerfile_template" ]; then
        copy_template "docker/Dockerfile.$dockerfile_template" "Dockerfile"
    else
        log_warning "No Dockerfile template found for $FRAMEWORK"
    fi
}

# Create README
create_readme() {
    [ "$CREATE_README" != true ] && return
    
    log_step "Creating README.md..."
    
    # Set template variables
    export PROJECT_NAME PROJECT_DESCRIPTION FRAMEWORK
    
    copy_template "README.md.tmpl" "README.md" '$PROJECT_NAME $PROJECT_DESCRIPTION $FRAMEWORK'
}

# Initialize git repository
init_git_repo() {
    [ "$INIT_GIT" != true ] && return
    
    log_step "Initializing git repository..."
    
    git init
    git checkout -b "$GIT_BRANCH"
    
    if [ -n "$GIT_ORIGIN" ]; then
        git remote add origin "$GIT_ORIGIN"
        log_success "Added git remote origin"
    fi
    
    # Create appropriate .gitignore
    local gitignore_template=""
    if [[ "$FRAMEWORK" == *"python"* ]] || [[ "$FRAMEWORK" == "django" ]] || [[ "$FRAMEWORK" == "fastapi" ]]; then
        gitignore_template="python"
    else
        gitignore_template="node"
    fi
    
    if [ -f "$TEMPLATES_DIR/gitignore/$gitignore_template" ]; then
        cp "$TEMPLATES_DIR/gitignore/$gitignore_template" .gitignore
        log_success "Created .gitignore"
    fi
    
    # Initial commit
    git add .
    git commit -m "feat: initial project setup"
    log_success "Created initial commit"
}

# Main execution
main() {
    check_dependencies
    
    # Check if project name is provided as argument
    if [ $# -eq 1 ]; then
        PROJECT_NAME="$1"
        echo "Using project name: $PROJECT_NAME"
        # You could extend this to support more CLI arguments
    fi
    
    # Get user input if not provided via CLI
    if [ -z "$PROJECT_NAME" ]; then
        get_user_input
    else
        # Still need other inputs
        get_user_input
    fi
    
    # Check if project directory already exists
    if [ -d "$PROJECT_NAME" ]; then
        log_error "Project directory '$PROJECT_NAME' already exists!"
        exit 1
    fi
    
    # Create project directory
    mkdir "$PROJECT_NAME"
    cd "$PROJECT_NAME"
    
    log_info "Creating project: $PROJECT_NAME"
    log_info "Framework: $FRAMEWORK"
    
    # Export variables for stack scripts
    export_variables
    
    # Execute the framework-specific stack script
    local stack_script="$STACKS_DIR/$FRAMEWORK.sh"
    if [ -f "$stack_script" ] && [ -x "$stack_script" ]; then
        log_step "Executing $FRAMEWORK stack script..."
        "$stack_script"
    else
        log_error "Stack script $stack_script not found or not executable!"
        exit 1
    fi
    
    # Setup common components
    setup_formatters
    setup_precommits
    setup_commitizen
    create_dockerfile
    create_readme
    init_git_repo
    
    echo
    log_success "Project '$PROJECT_NAME' created successfully!"
    log_info "Next steps:"
    echo "  1. cd $PROJECT_NAME"
    echo "  2. Start coding! 🚀"
}

# Run main function
main "$@"
