# our chamber image

FROM segment/chamber:2.8.2 AS chamber

# our build image

FROM python:3.7-buster AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip pip-tools

COPY requirements/requirements.txt /tmp/

RUN python3 -m venv /venv

RUN --mount=type=cache,target=/root/.cache \
    . /venv/bin/activate && \
    pip install --requirement /tmp/requirements.txt

WORKDIR /src

# ---------

# our release image

# TODO: change to python:3.7-slim-buster
FROM python:3.7-buster AS release

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip pip-tools

ENV PATH /venv/bin:/bin:/usr/bin:/usr/local/bin
ENV PYTHONDONTWRITEBYTECODE=true
ENV PYTHONPATH /src
ENV PYTHONUNBUFFERED 1
ENV PYTHONWARNINGS ignore

COPY --from=chamber /chamber /bin/chamber
COPY --from=builder /usr/lib/**/**.so.* /usr/lib/
COPY --from=builder /venv/ /venv/
COPY --from=builder /src/ /src/
COPY . /src/

WORKDIR /src
