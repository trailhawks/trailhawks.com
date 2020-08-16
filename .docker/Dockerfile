# syntax = docker/dockerfile:experimental

FROM segment/chamber:2.8.2 AS chamber


FROM python:2.7-buster AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements/base.txt /tmp/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r /tmp/requirements.txt
    # && rm -rf /root/.cache


FROM python:2.7-slim-buster AS final

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=builder /usr/local /usr/local
COPY --from=builder /root /root
COPY --from=chamber /chamber /bin/chamber

RUN /sbin/ldconfig

WORKDIR /src/

COPY . /src/
