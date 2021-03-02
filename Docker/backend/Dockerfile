FROM python:3.9.2-alpine

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code/
COPY requirements.txt /code/
RUN pwd
RUN pip install -r requirements.txt
COPY ./interview ./
COPY docker/backend/entrypoint.sh /
RUN chmod +x /entrypoint.sh
RUN pytest -x -v
