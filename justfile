# Just is a crossplatform task-runner, similar to make.
# And justfiles are equivalent to makefiles.  #
# Official docs:
#  - https://just.systems/man/en
#
# Usage:
#   > just --help
#   > just <taskname>
# # Notes: #  - Comments immediately preceding a recipe will appear in just --list:

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


# show packages
poetry-show:
    poetry show

# show outdated packages
poetry-show-outdated:
    poetry show --outdated

# export poetry-defined requirements to a pip-installable requirements-file
[linux]
poetry-export-requirements:
    @ poetry lock
    @ poetry export -f requirements.txt --output etc/requirements.txt
    @ cat etc/requirements-header.txt <(echo "") etc/requirements.txt > etc/temp.txt && mv etc/temp.txt etc/requirements.txt
    @ cp etc/requirements.txt requirements.txt
    @ echo -e "Updated etc/requirements.txt"

# switch to staging-branch and git pull to update
update-staging:
    git co staging
    git pull



# run pytest
pytest:
    bin/pytest tests

# run pytest with coverage
pytest-coverage:
    bin/pytest tests --color=yes --cov=tsc_sphinx --cov-report term-missing --cov-report html --cov-report xml --junit-xml='var/cache/coverage/pytest.xml'

alias pytest-cov := pytest-coverage

# run django-admin to create a superuser
django-createsuperuser:
    bin/django-admin createsuperuser

# run django-admin to create migrations
django-makemigrations:
    bin/django-admin makemigrations

# run django-admin to apply migrations
django-migrate:
    bin/django-admin migrate

# run django-admin to collect static files
django-collectstatic:
    bin/django-admin collectstatic

# run django-admin to collect static files with no input
django-collectstatic-noinput:
    bin/django-admin collectstatic --noinput

# run django-admin to run the development server
django-runserver:
    bin/django-admin runserver

# open the django-admin in browser
url-admin:
    @ xdg-open "http://127.0.0.1:8000/admin/"

# open the swagger-api in browser
url-swagger:
    @ xdg-open "http://127.0.0.1:8000/swagger/"

# open the redoc-api in browser
url-redoc:
    @ xdg-open "http://127.0.0.1:8000/redoc/"



# lint python-code with isort + black
lint: isort black


# run black
black:
    # black src/**.py
    black scouts_kampvisum_api/**/*.py

# run isort
isort:
    # isort src/**.py
    isort scouts_kampvisum_api/**/*.py



