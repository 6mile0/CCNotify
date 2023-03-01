FROM python:latest

WORKDIR /src
COPY ./src/requirements.txt /src/requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
