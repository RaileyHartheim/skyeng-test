FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt .
RUN apt-get update -y && \
    apt-get install -y netcat && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

ADD ./skyeng /app/backend
ADD ./docker /app/docker


RUN chmod +x /app/docker/backend/django-entrypoint.sh
RUN chmod +x /app/docker/backend/celeryworker-entrypoint.sh
RUN chmod +x /app/docker/backend/celerybeat-entrypoint.sh
