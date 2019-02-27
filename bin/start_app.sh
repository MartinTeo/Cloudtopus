#!/bin/bash
cd /home/ec2-user/Django_Application/MayhemFive/CLE
sudo service nginx start
gunicorn CLE.wsgi:application instead of runserver 0.0.0.0:8000