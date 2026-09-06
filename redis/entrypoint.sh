#!/bin/sh
set -e

envsubst < /usr/local/etc/redis/redis.conf.template > /usr/local/etc/redis/redis.conf

exec redis-server /usr/local/etc/redis/redis.conf

chmod +x redis/entrypoint.sh