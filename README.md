# PREN2 CubePiLer

This repository contains the code for the PREN2 project CubePiLer.

This README is a work in progress and will be updated as the project progresses.

## Instalation

### Raspberry Pi

**First setup only:** To clone the repository on the Raspberry Pi, you need to create a new ssh key and add it to the GitHub repository.

- Create a new ssh key on your Raspberry Pi with the following command: `ssh-keygen -t ed25519 -C "<name>@stud.hslu.ch"`
- Copy the public key: `cat ~/.ssh/id_ed25519.pub`
- Add the public key to the GitHub repository under [`Settings > Deploy keys`](https://github.com/danlivingston/PREN2/settings/keys)

```bash
git clone git@github.com:danlivingston/PREN2.git
```

Then you can run the following script inside the cloned folder to install all the required tools and dependencies:

```bash
./scripts/install.sh
```

Note: This does not install the required Python version. And does not work out of the box on Debian 11 based distros.

### Windows

For windows, you can use the following commands after [installing Python 3.11](https://www.python.org/downloads/) or higher:

```bash
python -m pip install pipx --user
python -m pipx install poetry
python -m pipx ensurepath

# Restart the terminal

poetry install
```

There may be issues installing certain dependencies on Windows, remove the dependencies from the `pyproject.toml` file temporarily and run `poetry install` again. Remember to mock the dependencies using `.env` if necessary.

## Configuration

To configure the application you can copy the `.env.example` file to `.env` and change the values to your needs. Mocking of the raspberry pi attached hardware can be done by setting the `MOCK` variable to `TRUE`. The image recognition can be mocked by setting the `MOCK_CUBES` variable to `TRUE`.

```bash
cp .env.example .env
```

## Usage

To run the application, use the following commands:

```bash
# Raspberry Pi
./scripts/run.sh

# Windows
./scripts/run.bat

# Or
poetry run python main.py
```

## Updating

To update the repository, use the following commands:

```bash
# Raspberry Pi
./scripts/update.sh

# Windows
./scripts/update.bat

# Or
git pull
poetry install
```

## Development

### Adding dependencies

To add a new dependency, use the following command:

```bash
poetry add <package>
```

### Removing dependencies

To remove a dependency, use the following command:

```bash
poetry remove <package>
```

### Formatting

We use [black](https://black.readthedocs.io/en/stable/) for formatting and [isort](https://pycqa.github.io/isort/) for sorting imports.

```bash
# Raspberry Pi
./scripts/format.sh

# Windows
./scripts/format.bat

# Or
poetry run isort
poetry run black .
```

### Linting

We use [flake8](https://flake8.pycqa.org/en/latest/) for linting together with [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear).

```bash
poetry run flake8
```

### Logging

We use [loguru](https://github.com/Delgan/loguru) for logging.

```python
from loguru import logger

logger.info("Hello, World!")
```

Logs are written to the `logs` directory (always with a log level of DEBUG) and are printed to the console (log level can be adjusted in `.env`).

The following table shows the severity levels and the corresponding logger methods:

| Level name | Severity value | Logger method |
|------------|----------------|---------------|
| TRACE      | 5              | logger.trace() |
| DEBUG      | 10             | logger.debug() |
| INFO       | 20             | logger.info() |
| SUCCESS    | 25             | logger.success() |
| WARNING    | 30             | logger.warning() |
| ERROR      | 40             | logger.error() |
| CRITICAL   | 50             | logger.critical() |
