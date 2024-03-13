# our chamber image

FROM segment/chamber:2.8.2 AS chamber

# our build image

FROM python:3.9-slim-buster AS builder

ENV PATH /venv/bin:$PATH
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

RUN python -m uv venv /venv

COPY requirements.txt /tmp/

RUN --mount=type=cache,target=/root/.cache,id=pip \
    . /venv/bin/activate && \
    uv pip install --requirement /tmp/requirements.txt

WORKDIR /src/

# ---------

# our release image

FROM builder AS release

COPY --from=chamber /chamber /bin/chamber

COPY . /src/

CMD ["/bin/bash", "/src/web-start.sh"]
