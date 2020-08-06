#!/bin/bash

#↓２つを環境変数から渡す。
#BASIC_AUTH_USER_NAME
#BASIC_AUTH_PASSWD

CRYPTPASS=`openssl passwd -crypt ${BASIC_AUTH_PASSWD}`

echo "${BASIC_AUTH_USER_NAME}:${CRYPTPASS}" > /etc/nginx/.htpasswd