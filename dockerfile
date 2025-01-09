ARG BASE_IMAGE=python:3.12-slim-bookworm

FROM $BASE_IMAGE

RUN apt-get update && apt-get install -y \
pkg-config \
build-essential \
python3-dev \
default-libmysqlclient-dev \
libffi-dev \
libjpeg-dev \
zlib1g-dev \
libfreetype6-dev \
openssh-client \
&& rm -rf /var/lib/apt/lists/*

RUN groupadd demostore && groupadd docker && useradd -g demostore -G docker -s /bin/sh -m demostore

USER demostore

WORKDIR /app

COPY --chown=demostore:demostore requirements.txt /app/

RUN pip3 install --no-cache-dir -r requirements.txt

COPY --chown=demostore:demostore . .

ENV DJANGO_SETTINGS_MODULE=myproject.settings_prod

CMD ["gunicorn", "back_end.wsgi"]

EXPOSE 8000