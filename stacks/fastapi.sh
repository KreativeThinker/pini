#!/bin/bash

# FastAPI Stack Setup Script

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() { echo -e "${BLUE}ℹ️  $1${NC}"; }
log_success() { echo -e "${GREEN}✅ $1${NC}"; }

log_info "Setting up FastAPI project..."

# Check for uv
if ! command -v uv &> /dev/null; then
    log_info "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc || source ~/.profile || true
fi

# Initialize uv project
uv init --no-readme

# Core dependencies
log_info "Installing FastAPI dependencies..."
uv add fastapi "uvicorn[standard]" python-multipart

# Dev dependencies
log_info "Installing development dependencies..."
uv add --dev pytest pytest-asyncio httpx

# Formatter dependencies
if [ "$ENABLE_FORMATTERS" = true ]; then
    log_info "Installing formatters..."
    uv add --dev black isort flake8 mypy
fi

# Commitizen
if [ "$INIT_COMMITIZEN" = true ]; then
    log_info "Installing commitizen..."
    uv add --dev commitizen
fi

# Create basic FastAPI structure
mkdir -p app/{api,core,models,schemas}

# Create main.py
cat > main.py << 'EOF'
from fastapi import FastAPI
from app.api import health

app = FastAPI(
    title="${PROJECT_NAME}",
    description="${PROJECT_DESCRIPTION}",
    version="0.1.0"
)

app.include_router(health.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Create health check endpoint
cat > app/__init__.py << 'EOF'
EOF

cat > app/api/__init__.py << 'EOF'
EOF

cat > app/api/health.py << 'EOF'
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "healthy"}
EOF

# Create core config
cat > app/core/__init__.py << 'EOF'
EOF

cat > app/core/config.py << 'EOF'
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "${PROJECT_NAME}"
    debug: bool = False
    
    class Config:
        env_file = ".env"

settings = Settings()
EOF

# Create empty model and schema files
touch app/models/__init__.py
touch app/schemas/__init__.py

# Update pyproject.toml with project info and scripts
#
# TODO: Replace author details from config variables
# TODO: Fix tool configurations
cat >> pyproject.toml << EOF

[project]
name = "${PROJECT_NAME}"
description = "${PROJECT_DESCRIPTION}"
authors = [{name = "Your Name", email = "your.email@example.com"}]
license = {text = "MIT"}
requires-python = ">=3.8"

[project.scripts]
dev = "uvicorn main:app --reload --host 0.0.0.0 --port 8000"
start = "uvicorn main:app --host 0.0.0.0 --port 8000"

[tool.black]
line-length = 100
target-version = ["py38"]

[tool.isort]
profile = "black"
line_length = 100

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
EOF

# Create .env file
cat > .env << 'EOF'
DEBUG=true
EOF

log_success "FastAPI project structure created!"
log_info "Run 'uv run dev' to start the development server"
