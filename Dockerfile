FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1
RUN mkdir /code
RUN mkdir /code/logs
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
