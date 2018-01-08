#!/bin/sh
killall -9 nginx
killall -9 nginx
pkill -9 -af uwsgi
service nginx restart
/usr/local/bin/uwsgi --emperor /usr/local/etc/nginx/uwsgi/vassals --uid www --gid www --daemonize /var/log/uwsgi/emperor_kanazuchi.log 
