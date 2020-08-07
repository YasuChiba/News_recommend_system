# !/bin/bash

usermod -u $USER_ID -o -m webuser
groupmod -g $GROUP_ID webuser

uwsgi --ini /webuser/web/uwsgi.ini