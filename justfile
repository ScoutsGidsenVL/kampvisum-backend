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
install: ensure-dirs create-venv symlink-venv-dirs upgrade-pip uv-sync


# create python39 virtual-environment
create-venv:
    PYENV_VERSION=3.11 python -m venv .venv


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


# install the dependencies from uv.lock
uv-sync:
    uv sync --python 3.11


# update uv.lock
uv-lock:
    uv lock


# show packages
uv-tree:
    uv tree

# show outdated packages
uv-tree-outdated:
    uv tree --outdated

# switch to staging-branch and git pull to update
update-staging:
    git co staging
    git pull
