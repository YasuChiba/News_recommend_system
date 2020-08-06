FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip 


COPY ./classification/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt