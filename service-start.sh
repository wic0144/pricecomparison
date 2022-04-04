#!/bin/bash
service mysql status | grep 'active (running)' > /dev/null 2>&1

if [ $? != 0 ]
then
        sudo service mysql restart > /dev/null
fi

service ssh status | grep 'active (running)' > /dev/null 2>&1

if [ $? != 0 ]
then
        sudo service ssh restart > /dev/null
fi
# service mysql start
# service ssh start 
service elasticsearch start 
service kibana start 
start-all.sh
start-master.sh
start-worker.sh spark://LAPTOP-NKV0VISO.localdomain:7077
