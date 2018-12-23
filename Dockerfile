FROM python:3.7.1-alpine3.8

RUN mkdir -p /app
COPY . /app

WORKDIR /app

RUN apk update && apk add --virtual build-dependencies build-base gcc wget git
RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
RUN pip install --upgrade pip && pip install -e .
RUN apk del build-dependencies

RUN apk add bash curl
RUN pip install --no-cache-dir gunicorn

RUN rm -rf /root/.cache

CMD [ "gunicorn", "-c", "/app/deployment/gunicorn.conf", "--log-config", "/app/deployment/logging.conf", "svc.api.app:create_app"]
