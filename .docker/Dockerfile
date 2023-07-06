# our chamber image

FROM segment/chamber:2.8.2 AS chamber

# our build image

FROM python:3.9-slim-buster AS builder

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN --mount=type=cache,target=/root/.cache \
    pip install --upgrade pip pip-tools

COPY requirements.txt /tmp/

RUN --mount=type=cache,target=/root/.cache \
    pip install --requirement /tmp/requirements.txt

WORKDIR /src/

# ---------

# our release image

FROM builder AS release

COPY --from=chamber /chamber /bin/chamber

COPY . /src/

CMD ["/bin/bash", "/src/web-start.sh"]
