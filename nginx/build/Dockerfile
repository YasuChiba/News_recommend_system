FROM nginx

RUN apt-get update
RUN apt-get install -y openssl


COPY ./nginx/build/basic_auth_setup.sh /bin
RUN chmod +x /bin/basic_auth_setup.sh