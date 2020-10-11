FROM python:3.9.0 as build-env

LABEL Author="Max Sivkov"
LABEL E-mail="maxsivkov@gmail.com"
LABEL version="0.0.1"
STOPSIGNAL SIGINT

WORKDIR /app

RUN python3 -m pip install virtualenv
RUN virtualenv -p `which python3` venv

COPY . ./
# https://pythonhosted.org/an_example_pypi_project/setuptools.html
RUN . venv/bin/activate && pip install --no-cache-dir . &&\
  find /app/venv \( -type d -a -name test -o -name tests \) -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) -exec rm -rf '{}' \+

FROM python:3.9-alpine
#ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "app:create_app()"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG 0
ENV HOST=0.0.0.0
ENV PORT=7080

RUN apk update && \
    apk --no-cache --update add libstdc++ && \
    rm -rf /var/cache/apk/*

WORKDIR /app
COPY --from=build-env /app /app
ENV PATH="/app/venv/bin:$PATH"

CMD . venv/bin/activate && exec flask run --port ${PORT} --host=${HOST} --no-reload