# fastapi_template

## Prerequisites

### uv

[uv](https://docs.astral.sh/uv/) is a Python package and project manager. It is used to install, update, and run dependencies in this project.

The easiest way to install uv is with this shell script on MacOS and Linux: `curl -LsSf https://astral.sh/uv/install.sh` or this powershell command on Windows: `powershell -c "irm https://astral.sh/uv/install.ps1 | iex"`.

You can then install the required dependnecies for this project with the command `uv pip install -r pyproject.toml --extra dev`.

For further information, view the [documentation](https://docs.astral.sh/uv/guides/) or execute `uv --help`.

### just

This tool uses [just](https://github.com/casey/just) as a task runner.

`just` will automatically be installed for you when you install the dev prerequisites with `uv`. You will need to boot into the virtual environment (with `source .venv/bin/activate`) for `just` to be runnable from the command line.

It provides headers for common actions you might take in this codebase. A common task you might run to see if your code meets the quality standards is `just check`.

To list all available tasks, execute `just --list`.

For further information, view the [documentation](https://just.systems/man/en/) or execute `just --help`.

### Tooling

- [black](https://github.com/psf/black): Used to enforce common code formatting. This can be executed with `just format`.
- [pylint](https://pylint.readthedocs.io/en/stable/): Used to run simple code quality checks. This can be executed using `just lint` (to run all the linters) or `just pylint` (to just run pylint).
- [pyright](https://github.com/microsoft/pyright): This uses python type hints in "strict" mode. This check can be run using `just pyright` and is invoked during `just lint` as well.
  - This is installed with `uv` but requires that you have a recent version of Node installed. To do that, the easiest way is through `nvm`, with instructions available [here](https://github.com/nvm-sh/nvm?tab=readme-ovfile#installing-and-updating)
- [pytest](https://docs.pytest.org/en/stable/): This uses pytest to define and enforce behaviors. Tests can be executed with `just test`.
- [docker](https://www.docker.com): This project is deployed using docker containers. After installing docker, `just package` will produce the container and `just rundocker` will launch the project in a container.

### Fastapi

This project uses [FastAPI](https://fastapi.tiangolo.com) as its web framework. The service can be launch either through the default just target (simply run `just`) or through `just run`.

### Project format

- .github/workflows
    - This project uses GitHub Actions to do its CI/CD. Workflows are defined here.
- app/
    - Application entrypoints. FastAPI main is located here.
- frontend/
    - Static files and jinja templates for a browser frontend
- scripts/
    - Utilities scripts and tools to make use of this easier.
- src/
    - Contains the majority of the source that drives the application.
- tests/
    - Contains tests that exercise the boundaries of the application. Defines and defends the API and expectations around its behavior.
