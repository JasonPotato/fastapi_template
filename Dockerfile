FROM ghcr.io/astral-sh/uv:python3.10-alpine

ARG APP_USER=template_service
ARG APP_GROUP=template_service_group
ARG HOME_DIR=/home/${APP_USER}
ARG DEPLOY_DIR=${HOME_DIR}/deploy

ENV SERVICE_PORT=8000

# setup runtime user
RUN addgroup -S ${APP_GROUP} && adduser -S ${APP_USER} -G ${APP_GROUP}
USER ${APP_USER}

RUN mkdir ${DEPLOY_DIR}
WORKDIR ${DEPLOY_DIR}

ENV PATH="$PATH:${HOME_DIR}/.local/bin"

# install project dependencies
COPY pyproject.toml uv.lock .python-version justfile ./
RUN uv sync --frozen --no-install-project --no-dev
ENV PATH=".venv/bin:$PATH"

# copy project source into container
COPY ./src/ ./src/
COPY ./app/ ./app/
COPY ./scripts/health_check.py ./scripts/health_check.py
COPY ./scripts/pyproject_parser.py ./scripts/pyproject_parser.py

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 CMD uv run scripts/health_check.py --port ${SERVICE_PORT}

# reset entrypoing, don't invoke `uv`
ENTRYPOINT [ ]

CMD ["/bin/sh", "-c", "just --set service_ip 0.0.0.0 run"]
