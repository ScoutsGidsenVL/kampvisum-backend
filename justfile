# Just is a crossplatform task-runner, similar to make.
# And justfiles are equivalent to makefiles.
#
# Official docs:
#  - https://just.systems/man/en
#
# Usage:
#   > just --help
#   > just <taskname>
#
# Notes:
#  - Comments immediately preceding a recipe will appear in just --list:

# load environment variables from .env file
set dotenv-filename := ".env"
set dotenv-load       := true


# Help target
help:
    @ just --list --unsorted


# create directiries
ensure-dirs:
    @ mkdir -p var/cache
    @ mkdir -p var/log
    @ mkdir -p var/run
    @ mkdir -p var/static
    @ mkdir -p var/tmp


# full initial pythondev-installation
install: ensure-dirs create-venv symlink-venv-dirs upgrade-pip poetry-install


# create python39 virtual-environment
create-venv:
    PYENV_VERSION=3.9 python -m venv .venv


# symlink venv-dirs to make bin/python work
symlink-venv-dirs:
    @ ln -sf .venv/bin
    @ ln -sf .venv/lib
    @ ln -sf .venv/pyvenv.cfg


# symlink ipython to ip
symlink-ipython:
    @ cd .venv/bin && ln -sf ipython ip


# upgrade pip itself
upgrade-pip:
    bin/pip install -U pip


# run poetry install
poetry-install:
    poetry install


# update poetry.lock
poetry-lock:
    poetry lock

# export poetry-defined requirements to a pip-installable requirements-file
[linux]
poetry-export-requirements:
    @ poetry lock
    @ poetry export -f requirements.txt --output etc/requirements.txt
    @ cat etc/requirements-header.txt <(echo "") etc/requirements.txt > etc/temp.txt && mv etc/temp.txt etc/requirements.txt
    @ cp etc/requirements.txt requirements.txt
    @ echo -e "Updated etc/requirements.txt"
