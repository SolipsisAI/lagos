FROM ubuntu:22.04

RUN apt-get -y update
RUN apt-get install python3 -y
RUN apt-get install python3-pip -y  

WORKDIR /app
ADD ./builds/ /app/builds

RUN pip install /app/builds/*.whl