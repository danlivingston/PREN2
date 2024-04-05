#!/bin/bash
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip pipx python-is-python3

pipx install poetry
pipx ensurepath

source ~/.bashrc
cd "$(dirname "$0")/.."
poetry install

echo -e "\n\033[0;31m!!! Please restart your terminal to complete installation !!!\033[0m\n"
