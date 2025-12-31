# syntax = docker/dockerfile:experimental
# Uses Docker BuildKit for improved caching and build performance

# ------------------------------------------------------------
# Stage 1: Import chamber (secrets management tool)
# ------------------------------------------------------------
FROM segment/chamber:2.14 AS chamber

# ------------------------------------------------------------
# Stage 2: Base/builder layer - Setup Python environment
# ------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /src
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

# Update the package list and install git and curl
RUN --mount=type=cache,target=/var/cache/apt,rw \
    --mount=type=cache,target=/var/lib/apt,rw \
    apt-get update && apt-get install -y build-essential git curl

COPY pyproject.toml uv.lock /tmp/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --directory /tmp

WORKDIR /src/

# ---------

# our release image

FROM builder AS release

COPY --from=chamber /chamber /bin/chamber

COPY . /src/

CMD ["/bin/bash", "/src/web-start.sh"]
