# FastAPI Bootstrap

This FastAPI bootstrap template shows how to build cloud-native APIs with built-in OpenAPI documentation.

## Development Setup

These APIs are written using Python 3.9 and the [FastAPI](https://fastapi.tiangolo.com/) framework and dependencies are managed with [Poetry](https://python-poetry.org/docs/master/).
The `cmd.sh` helper script is written for usage with a unix based bash shell which is the default on Mac and Linux but within Windows you will need to utilize a [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/install-win10) setup.

Verify you have python 3.9 installed.

```bash
# python3 --version
Python 3.9.12
```

Then you need to install poetry which will manage dependencies and the python virtual environment.

```bash
# curl -sSL https://install.python-poetry.org | python3 -
```

Install the required development and production project dependencies.

```bash
# poetry install
```

You will need to have the production `.env` file in the root of the project in order to authenticate, connect to DBs, etc. and the required keys can be checked in the `.env-example` file.
Start the development server which will reload as changes are made and access the OpenAPI frontend at <http://localhost:8000>

```bash
# ./cmd.sh start
Dev API Docs: http://localhost:8000

INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
[2022-07-12 10:24:02,278] INFO [uvicorn.error.bind_socket:564] Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [24473] using watchgod
[2022-07-12 10:24:02,283] INFO [uvicorn.error.startup:56] Started reloader process [24473] using watchgod
INFO:     Started server process [24476]
[2022-07-12 10:24:02,533] INFO [uvicorn.error.serve:75] Started server process [24476]
INFO:     Waiting for application startup.
[2022-07-12 10:24:02,533] INFO [uvicorn.error.startup:45] Waiting for application startup.
INFO:     Application startup complete.
[2022-07-12 10:24:02,533] INFO [uvicorn.error.startup:59] Application startup complete.
```

## Code Quality

Code consistency, quality and formatting is maintained with the following tools.

- [black](https://black.readthedocs.io/en/stable/)
- [flake8](https://flake8.pycqa.org/en/latest/)
- [isort](https://pycqa.github.io/isort/)

The `./cmd.sh format` command can be ran to format the project files which runs the tools with the following options. Most IDEs allow a `format on save` feature which is convient to setup with these configurations as well.

```bash
python3 -m isort --multi-line 3 --trailing-comma --line-length 79 app
python3 -m flake8 --max-line-length=79 app
python3 -m black --line-length=79 app
```

## Best Practices

- Include type hints for the parameters on functions
- Include docstrings on functions
- Minimize the number of funcitons in a single file instead opt for addional files with relevant names.
- Add pydantic models and enums within their own file for each API router

## Deployment

- Update the version in [pyproject.toml](./pyproject.toml)
- Update the container image to the new version in [deployment.yaml](./k8s/deployment.yaml)
- Update the [CHANGELOG.md](./CHANGELOG.md) with the updates in the new version
- Create and push the new version tag
  - `git tag v1.0.2 && git push origin -u v1.0.2`

## Available Scripts

In the project directory, you can run:

### `./cmd.sh format`

Runs the black, flake8 and isort tools to allow consistent formatting

### `./cmd.sh test`

Runs all tests available.

### `./cmd.sh start`

Runs the app locally with uvicorn in development mode.  
Open [http://localhost:8000](http://localhost:8000) to view it in the browser.

The server will reload as you make edits but you may need to reload the swagger documentation.
