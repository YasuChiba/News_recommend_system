FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip libmysqlclient-dev mysql-client curl


RUN apt-get install -y \
        build-essential \
        wget \
        git \
        unzip \
        gcc \
        zlib1g-dev \
        && rm -rf /var/cache/apk/*

RUN git clone https://github.com/facebookresearch/fastText.git /tmp/fastText && \
    cd /tmp/fastText && \ 
    make


#mecab
RUN apt-get install -y mecab mecab-ipadic-utf8 libmecab-dev swig




COPY ./classification/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt