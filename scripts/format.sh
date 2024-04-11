#!/bin/bash
cd "$(dirname "$0")/.."
echo "running isort..."
poetry run isort .
echo "running black..."
poetry run black .
echo "done"
