FROM*.py[cod] python:3.12-alpine

WORKDIR /backend

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . /backend

ENV PYTHONPATH=/backend

EXPOSE 8000
