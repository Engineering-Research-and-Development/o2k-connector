FROM python:3.9.13-bullseye
LABEL version="0.1"

COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

RUN mkdir /o2k-connector
RUN mkdir /o2k-connector/data
RUN mkdir /o2k-connector/logs

COPY . /o2k-connector

WORKDIR /o2k-connector

ENTRYPOINT ["python3", "app.py"]
