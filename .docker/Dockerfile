# syntax = docker/dockerfile:experimental

FROM segment/chamber:2.8.2 AS chamber


FROM python:2.7-buster AS dev
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements/base.txt /tmp/requirements.txt

# RUN --mount=type=cache,target=/root/.cache/pip pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /src/

FROM dev AS production

COPY --from=chamber /chamber /bin/chamber

COPY . /src/
