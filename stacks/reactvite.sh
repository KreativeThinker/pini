#!/bin/bash

set -e

PROJECT_NAME=$1

pnpm create vite@latest "$PROJECT_NAME" -- --template react
cd "$PROJECT_NAME"

pnpm install
git init
npx commitizen init cz-conventional-changelog --save-dev --save-exact

# Add configs (copy from templates later)
