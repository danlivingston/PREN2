@echo off
cd /d "%~dp0.."
git pull
poetry install