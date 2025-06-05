#!/bin/bash
set -e

PROJECT_NAME=$1

mkdir "$PROJECT_NAME"
cd "$PROJECT_NAME"

uv venv
source .venv/bin/activate

uv pip install django djangorestframework
django-admin startproject core .

git init
cz init

# Add config copies later
