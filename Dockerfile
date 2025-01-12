FROM python:3.12-slim-bookworm

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

ENV PATH="/home/demostore/.local/bin:$PATH"

ENV DJANGO_SETTINGS_MODULE=back_end.settings.prod

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "back_end.wsgi"]

EXPOSE 8000