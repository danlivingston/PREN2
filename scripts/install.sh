#!/bin/bash

# bullseye alternate?
# download python, install tk-dev, build python, install pipx with python -m pip

sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip pipx python-is-python3

pipx install poetry
pipx ensurepath

source ~/.bashrc
cd "$(dirname "$0")/.."
poetry install

sudo rm /etc/systemd/system/cubepiler.service
sudo ln -s "$(pwd)/cubepiler.service" /etc/systemd/system/cubepiler.service
sudo systemctl daemon-reload
sudo systemctl enable cubepiler
sudo systemctl start cubepiler

echo -e "\n\033[0;31m!!! Please restart your terminal to complete installation !!!\033[0m\n"
