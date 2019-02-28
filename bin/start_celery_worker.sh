#!/bin/bash
clear
cd /home/ec2-user/Cloudtopus/CLE
celery -A CLE worker --pool=eventlet
