FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip 


COPY ./web/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY ./web/build/start.sh /bin
RUN chmod +x /bin/start.sh

#これを設定しないPythonで日本語を扱えない
ENV PYTHONIOENCODING utf-8


