#!/bin/bash
set -e

PROJECT_NAME=$1

mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"

uv venv
source .venv/bin/activate

touch main.py

git init
cz init

# Add config copies later
