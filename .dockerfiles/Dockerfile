# syntax = docker/dockerfile:experimental
# Uses Docker BuildKit for improved caching and build performance

# ------------------------------------------------------------
# Stage 1: Import chamber (secrets management tool)
# ------------------------------------------------------------
FROM segment/chamber:2.14 AS chamber

# ------------------------------------------------------------
# Stage 2: Base/builder layer - Setup Python environment
# ------------------------------------------------------------
FROM python:3.12-slim-bookworm AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONPATH /src
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

# Update the package list and install git
RUN --mount=type=cache,target=/var/cache/apt,rw \
    --mount=type=cache,target=/var/lib/apt,rw \
    apt-get update && apt-get install -y build-essential git

RUN --mount=type=cache,target=/root/.cache,id=pip \
    pip install --upgrade pip uv

COPY requirements.txt /tmp/

RUN --mount=type=cache,target=/root/.cache,id=pip \
    python -m uv pip install --system --requirement /tmp/requirements.txt

WORKDIR /src/

# ---------

# our release image

FROM builder AS release

COPY --from=chamber /chamber /bin/chamber

COPY . /src/

CMD ["/bin/bash", "/src/web-start.sh"]
