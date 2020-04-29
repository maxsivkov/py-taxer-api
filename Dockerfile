FROM python:3.8.2

LABEL Author="Max Sivkov"
LABEL E-mail="maxsivkov@gmail.com"
LABEL version="0.0.1"
STOPSIGNAL SIGINT

RUN apt-get -y update && apt-get install -y jq\
	&& rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m pip install virtualenv
RUN virtualenv -p `which python3` venv

COPY . ./
# https://pythonhosted.org/an_example_pypi_project/setuptools.html
RUN . venv/bin/activate && python setup.py develop

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "app:create_app()"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG 0
ENV HOST=0.0.0.0
ENV PORT=7080

CMD . venv/bin/activate && exec flask run --port ${PORT} --host=${HOST} --no-reload