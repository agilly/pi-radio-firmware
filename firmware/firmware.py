#!/usr/bin/env python

from llist import *
import sys
import time
from rotary_class import RotaryEncoder
import subprocess
import datetime
import os

radiolist="/home/admin/pi-radio-firmware/firmware/radiolist"
station_ring=dllist()
ENCODER_STATE=0
PLAY_STATE=34
WAIT_STATE=77
PIN_A = 14 	# Pin 8 
PIN_B = 15	# Pin 10
BUTTON = 4	# Pin 7
LATENCY=0.05
CURRENT_STATE=0
ARMED=1
process=0

now=datetime.datetime.now()
WAKE_TIME=now.replace(hour=6, minute=50, second=0, microsecond=0)
if now > WAKE_TIME:
	ARMED=0

def switch_event(event):
	global ENCODER_STATE
	if event == RotaryEncoder.CLOCKWISE:
		ENCODER_STATE=1
	elif event == RotaryEncoder.ANTICLOCKWISE:
		ENCODER_STATE=2
	elif event == RotaryEncoder.BUTTONDOWN:
		ENCODER_STATE=3
	return

rswitch = RotaryEncoder(PIN_A,PIN_B,BUTTON,switch_event)


def initializeStationRing():
	f=open(radiolist, 'r')
	for line in f:
		station_ring.append(line.replace("\n", ""))


def waitState():
	global PLAY_STATE
	global ENCODER_STATE
	global ARMED
	global LATENCY
	global WAKE_TIME
	print "\n\n=====WAIT STATE====\n\n"
	while True:
		time.sleep(LATENCY*5)
		now=datetime.datetime.now()
		
		if (ARMED==0 and datetime.datetime.now().time() < WAKE_TIME.time()):
			ARMED=1
			
		if ( ENCODER_STATE == 3 or ( now.time() > WAKE_TIME.time() and ARMED==1 and now.weekday() < 5) ) : #now.weekday() <10
			ENCODER_STATE=0
			time.sleep(10*LATENCY)
			if ( now.time() > WAKE_TIME.time()  ):
				ARMED=0;
			return PLAY_STATE
	return -1

def playState():
	global ENCODER_STATE
	global LATENCY
	global PLAY_STATE
	global WAIT_STATE
	global process;
	print "\n\n=====PLAY STATE=====\n\n"
	value=station_ring.first.value
	valuet=value.split("\t")
#       	command= '/home/pi/speak'+valuet[1]+'.sh '+valuet[2]+'&& exec mpg321 '+valuet[0]+' -a hw:0,0'
	command='exec mpg321 /home/pi/'+valuet[2]+ '.mp3'
	commandb='exec mpg321 '+ valuet[0]+' -a hw:0,0'
	print command
	if process!=0:
#       		os.system("killall mpg321")
		process.kill()
		process.wait()
		time.sleep(5*LATENCY)
	process=subprocess.Popen(command, shell=True)
	process.wait()
	process=subprocess.Popen(commandb, shell=True)
	while True:
		time.sleep(LATENCY)
		if ENCODER_STATE==1:
			process.kill()
#			os.system("killall mpg321")
			print "\n\n====SCROLL CLK : KILLING CHILD====\n\n"
			process.wait()
			print "==============================DONE"
			time.sleep(10*LATENCY)
			station_ring.rotate(1)
			value=station_ring.first.value
			valuet=value.split("\t")
#			command= '/home/pi/speak'+valuet[1]+'.sh '+valuet[2]+'&& exec mpg321 '+valuet[0]+' -a hw:0,0'
			command='exec mpg321 /home/pi/'+valuet[2]+'.mp3'
			commandb='exec mpg321 '+valuet[0]+' -a hw:0,0'
			print command
			process=subprocess.Popen(command, shell=True)
			process.wait()
			process=subprocess.Popen(commandb, shell=True)
			ENCODER_STATE=0
		if ENCODER_STATE==2:
			print "\n\n====SCROLL ANTCLK : KILLING CHILD====\n\n"
			process.kill()
#			os.system("killall mpg321")
			process.wait()
			print "==============================DONE"
			time.sleep(10*LATENCY)
			station_ring.rotate(-1)
#			process=subprocess.Popen('exec mpg321 '+ station_ring.first.value+ ' -a hw:0,0', shell=True)
			value=station_ring.first.value
			valuet=value.split("\t")
#			command= '/home/pi/speak'+valuet[1]+'.sh '+valuet[2]+'&& exec mpg321 '+valuet[0]+' -a hw:0,0'
			command='exec mpg321 /home/pi/'+valuet[2]+'.mp3 '
			commandb='exec mpg321 '+valuet[0]+' -a hw:0,0'
			print command
			process=subprocess.Popen(command, shell=True)
			process.wait()
			process=subprocess.Popen(commandb, shell=True)
			ENCODER_STATE=0
		if ENCODER_STATE==3:
			print "\n\n======BTN PRESS: KILL ALTOGETHER============\n\n"
			process.kill()
			process.wait()
#			os.system("killall mpg321")
			print "==============================DONE"
			time.sleep(10*LATENCY)
			ENCODER_STATE=0
			process=0
			return WAIT_STATE


initializeStationRing()

while True:
	print "Main state test...\n"
	if CURRENT_STATE==0 :
		CURRENT_STATE=waitState()
	if CURRENT_STATE==PLAY_STATE:
		CURRENT_STATE=playState()
	if CURRENT_STATE==WAIT_STATE :
		CURRENT_STATE=waitState()

