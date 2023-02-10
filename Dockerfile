FROM python:3.11

WORKDIR /app
RUN pip install --no-cache-dir Flask gunicorn

COPY ./pub_keys.json /app
COPY /templates /app/templates
COPY ./mqtt_connection.py /app
COPY ./gunicorn.conf.py /app
COPY ./app.py /app

RUN useradd -s /bin/bash admin
RUN chown -R admin /app

USER admin
ENV GUNICORN_CMD_ARGS="--bind=0.0.0.0:9000 --threads=4 --worker-class=gthread -c gunicorn.conf.py"
EXPOSE 9000
CMD ["gunicorn", "app:app"]