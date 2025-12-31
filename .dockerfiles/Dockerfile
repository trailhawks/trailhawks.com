# syntax = docker/dockerfile:experimental
# Uses Docker BuildKit for improved caching and build performance

# ------------------------------------------------------------
# Stage 1: Import chamber (secrets management tool)
# ------------------------------------------------------------
FROM segment/chamber:2.14 AS chamber

# ------------------------------------------------------------
# Stage 2: Base/builder layer - Setup Python environment
# ------------------------------------------------------------
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Copy chamber for secrets management in production
COPY --from=chamber /chamber /bin/chamber

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

RUN apt-get update && \
    apt-get install -y build-essential curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /src

WORKDIR /src

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-install-project --no-dev

COPY . /src/

# Install the project itself
RUN uv sync --frozen --no-dev

EXPOSE 8000

CMD ["/src/start-web.sh"]
