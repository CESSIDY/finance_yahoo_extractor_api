FROM python:3.9

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./finance_yahoo_extractor_api /app
WORKDIR /app
