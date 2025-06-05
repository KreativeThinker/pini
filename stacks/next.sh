#!/bin/bash
set -e

PROJECT_NAME=$1

pnpm create next-app "$PROJECT_NAME" --ts
cd "$PROJECT_NAME"

pnpm install
git init
npx commitizen init cz-conventional-changelog --save-dev --save-exact

# Add config copies later
