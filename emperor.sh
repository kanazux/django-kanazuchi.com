#!/bin/sh
pkill -9 nginx
pkill -9 uwsgi
service nginx restart
/usr/bin/uwsgi --emperor /usr/local/etc/nginx/uwsgi/vassals --uid www --gid www --daemonize /var/log/uwsgi/emperor_kanazuchi.log
