#!/bin/bash
echo "running isort..."
poetry run isort .
echo "running black..."
poetry run black .
echo "done"