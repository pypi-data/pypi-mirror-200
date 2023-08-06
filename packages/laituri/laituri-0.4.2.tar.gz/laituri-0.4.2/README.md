# laituri — Docker Toolkit for Python

[![CI](https://github.com/valohai/laituri/actions/workflows/ci.yml/badge.svg)](https://github.com/valohai/laituri/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/valohai/laituri/branch/master/graph/badge.svg)](https://codecov.io/gh/valohai/laituri)

`laituri` is a set of Docker-related Python snippets used at [Valohai](https://valohai.com/).
You can use it with Python >= 3.7.

## Usage

### Configuration

You can configure your used Docker command if it is not the default `docker`, using laituri settings.

_Example:_

```
laituri.settings.DOCKER_COMMAND = 'docker'
```

### Docker Credential Manager

Laituri contains a docker credentials manager which can be used for example when pulling images.
It logs in and out using the Docker CLI.

_Example:_

```
from laituri.docker.credential_manager import get_credential_manager

my_credentials = {
    'username': 'SmolShark1',
    'password': 'sharksWithLazers',
}

with get_credential_manager(
    image='python:latest',
    registry_credentials=my_credentials,
    log_status=print  # Any callable
):
    # Do your docker things!
```

## Development

Installing editable library version in the current virtual environment.

```bash
# install this package and all development dependencies
pip install -e . -r requirements-dev.txt pip-tools pre-commit && pre-commit install

# manually run lint and type checks
pre-commit run --all-files

# manually run tests
pytest --cov

python
>>> import laituri; print(laituri.__version__)
```

## Making a Release

A new release build is released by the CI when a new tag is pushed to the repository:

```bash
# bump version number in "laituri/__init__.py"
vim laituri/__init__.py

# pushing a new tag will trigger a new release build
git add .
git commit -m "Become to X.Y.Z"
git tag -a vX.Y.Z -m "Version X.Y.Z"
git push --follow-tags
```

If a manual release is needed, you can follow up the above steps with:

```bash
pip install build twine
git clean -fdx -e .idea/
python -m build .
twine upload dist/*
```
