default: check run

fail_on_format_diff := "false"
format_checks := if fail_on_format_diff =="true" { "--check --diff" } else { "" }

python_source := "./app/ ./src/ ./tests/ ./scripts/"
pythonpath_value := "./app/:./src/:./scripts/"

yaml_source := ".yamllint ./.github/workflows/"

service_ip := "localhost"
service_port := "8000"

fastapi_run_mode := "dev"

image_name := `uv run scripts/pyproject_parser.py name`
image_version := "v"+`uv run scripts/pyproject_parser.py version`
container_name:= 'template_app'

run:
    @PYTHONPATH={{pythonpath_value}} uv run --no-dev fastapi {{fastapi_run_mode}} app/main.py --proxy-headers --host {{service_ip}} --port {{service_port}}

stopdocker:
    @docker rm -f {{container_name}} 2>/dev/null 1>/dev/null

rundocker: package stopdocker
    @docker run --detach --name {{container_name}} --publish {{service_port}}:{{service_port}} {{image_name}}:{{image_version}}

check: format lint test

format:
    @uv run black {{python_source}} {{format_checks}}

lint: yamllint dockerlint pythonlint

pythonlint: pylint pyright

pylint:
    @uv run pylint {{python_source}}

pyright:
    @PYTHONPATH={{pythonpath_value}} uv run pyright {{python_source}}

yamllint:
    @uv run yamllint {{yaml_source}}

dockerlint:
    @uv run hadolint Dockerfile

test:
    @uv run pytest

package:
    @docker build -t {{image_name}}:{{image_version}} .

clean:
    git clean -dxff
    uv sync
