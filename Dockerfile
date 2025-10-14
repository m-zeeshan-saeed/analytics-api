
FROM python:3.11.14-slim

ARG PROJ_NAME="main"

RUN python -m venv /opt/venv

ENV PATH=/opt/venv/bin:$PATH

RUN pip install --upgrade pip

RUN apt-get update && apt-get install -y libpq-dev libjpeg-dev libcairo2 git gcc && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

COPY requirements.txt /tmp/requirements.txt

COPY ./src /code

RUN pip install -r /tmp/requirements.txt

COPY ./boot/docker-run.sh /opt/run.sh

RUN chmod +x /opt/run.sh

RUN apt-get remove --purge -y && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

CMD ["/opt/run.sh"]
