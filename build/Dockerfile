FROM python:3.9.13-bullseye
LABEL version="0.1"

RUN apt-get update
RUN  apt-get install -y --no-install-recommends nano gcc git libssl-dev g++ make && \
  cd /tmp && git clone https://github.com/edenhill/librdkafka && \
  cd librdkafka && git checkout tags/v2.0.2 && \
  ./configure && make && make install && \
  ldconfig && \
  cd ../ && rm -rf librdkafka

COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt

RUN mkdir /o2k-connector
RUN mkdir /o2k-connector/data
RUN mkdir /o2k-connector/logs

COPY . /o2k-connector

WORKDIR /o2k-connector

ENTRYPOINT ["python3", "app.py"]
