FROM python:3.11-slim

WORKDIR /app
COPY app/requirements.txt /app/requirements.txt

RUN apt-get update \
    && apt-get install -y build-essential git curl \
    && pip install --upgrade pip \
    && pip install -r /app/requirements.txt \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY app/ /app/

ENV PYTHONUNBUFFERED=1
EXPOSE 5000 8001