#!/usr/bin/env/python

import os
import paho.mqtt.client as mqtt
from time import sleep
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

SleepTimeL = 0.2

pinList = [2,3,4,17,18,27,22,23,24,25,10,9,11,7,8]

for i in pinList:
	GPIO.setup(i, GPIO.OUT)
	GPIO.output(i, GPIO.HIGH)

# The callback for when the client receives a CONNACK response from the server.
def main():
  def on_connect(client, userdata, flags, rc):
	client.subscribe("/door/cmd/#")
  def on_message(client, userdata, msg):
	if msg.topic == "/door/cmd/lock" :
		if msg.payload == "ON" :
			GPIO.output(4, GPIO.HIGH)
			time.sleep(1);
			GPIO.output(4, GPIO.LOW)
			print "Door Lock Switched"
	if msg.topic == "/home/test/2" :
		if msg.payload == "ON" :
			GPIO.output(3, GPIO.LOW)
			time.sleep(SleepTimeL);
			#print "Outlet 2 On"
		if msg.payload == "OFF" :
			GPIO.output(3, GPIO.HIGH)
			time.sleep(SleepTimeL);
			#print "Outlet 2 Off"

  client = mqtt.Client()
  client.on_connect = on_connect
  client.on_message = on_message
  client.username_pw_set(username=admin, password=password)

  client.connect("MQTT BROKER IP ADDRESS", 1883, 60)

  client.loop_forever()

if __name__ == '__main__':
	try:
	  	main()
	except KeyboardInterrupt:
		GPIO.cleanup()
