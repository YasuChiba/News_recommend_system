FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y python3 python3-pip curl sudo



RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get install -y nodejs


RUN npm install -g @vue/cli
RUN npm install -g axios
RUN npm install -g vue-router



COPY ./web/requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

COPY ./web/build/start.sh /bin
RUN chmod +x /bin/start.sh

#これを設定しないPythonで日本語を扱えない
ENV PYTHONIOENCODING utf-8


# 一般ユーザーアカウントを追加
RUN useradd -m webuser
# 一般ユーザーにsudo権限を付与
RUN gpasswd -a webuser sudo
# 一般ユーザーのパスワード設定
RUN echo "webuser:passwd" | chpasswd

