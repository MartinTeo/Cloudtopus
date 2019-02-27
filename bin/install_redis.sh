#!/bin/bash
#installs tcl dependencies
sudo yum install -y tcl
#installation of redis
wget http://download.redis.io/releases/redis-4.0.11.tar.gz
tar xzf redis-4.0.11.tar.gz
cd redis-4.0.11
make
sudo make test install
redis-server