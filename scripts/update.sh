#!/bin/bash
cd "$(dirname "$0")/.."
git pull
poetry install
