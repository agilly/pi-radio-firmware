#!/bin/bash

## This script is intended to be run as a service. It makes sure the internet connection is active. If it is not, it will restart the interface.

NUMTRY=3
DELAY=1

response=$(ping -c1 8.8.8.8 | grep "1 received")
trial=0

while true ; do
if [ -z "$response" ];
then
	# Google.com is not responding. Try three times.
	if [ $trial -lt $NUMTRY ]; then
        	trial=$(( trial + 1 ))
		echo [$(date)] YOU LOOK A BIT DOWN, TRIAL $trial
        	sleep 1
        else
        	# We tried enough. Restart iface.
		trial=0
		echo [$(date)] RESTART
		echo [$(date)] DOWN
		ifdown wlan0
		sleep 5
		echo UP
		ifup --force wlan0
		sleep 20
		echo [$(date)] RETRY
        fi
elif [ $trial -gt 1 ]; then
	echo [$(date)] ALL GOOD NOW.
	trial=1
fi
sleep $DELAY
response=$(ping -c1 8.8.8.8 | grep "1 received")
done
