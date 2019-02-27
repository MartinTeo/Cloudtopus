#!/bin/bash
clear
cd /home/ec2-user/Django_Application/MayhemFive/CLE
celery -A CLE beat -l info
