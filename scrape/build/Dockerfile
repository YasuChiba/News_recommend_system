FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip libmysqlclient-dev mysql-client cron vim curl

#selenium用のchromedriver
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable=84.0.4147.105-1


COPY ./scrape/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

#cronの設定ファイル
COPY ./scrape/build/cron_scrape /etc/cron.d
RUN chmod 644 /etc/cron.d/cron_scrape

#これを設定しないPythonで日本語を扱えない
ENV PYTHONIOENCODING utf-8



