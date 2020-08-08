# !/bin/bash

usermod -u $USER_ID -o -m webuser
groupmod -g $GROUP_ID webuser

export PYTHONIOENCODING=utf-8
uwsgi --ini /webuser/web/uwsgi.ini