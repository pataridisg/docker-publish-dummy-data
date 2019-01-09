#------------------------------------------
#--- Original Author: Pradeep Singh
#--- Date: 20th January 2017
#--- Version: 1.0
#--- Python Ver: 2.7
#--- Details At: https://iotbytes.wordpress.com/store-mqtt-data-from-sensors-into-sql-database/
#--- Changed by Pataridis Georgios 12/2018
#------------------------------------------


import paho.mqtt.client as mqtt
import random, threading, json
from datetime import datetime
import time


def on_connect(client, userdata, flags, rc):
	if rc==0:
		client.connected_flag=True #set flag
		print("connected OK")
	else:
		print("Bad connection Returned code=",rc)

def on_publish(client, userdata, mid):
	pass


def on_disconnect(client, userdata, rc):
	if rc !=0:
		pass


#====================================================
# MQTT Settings 
mqtt.Client.connected_flag=False	#create flag in class
broker="192.168.1.10"
port = 1883 
user = "dummy"
password = "dummy"
MQTT_Topic_Humidity = "dummyhum1"
MQTT_Topic_Temprature = "dummytemp1"

#====================================================

mqtt.Client.connected_flag=False	#create flag in clas

client = mqtt.Client("pythondummy1")
client.username_pw_set(user, password=password)    	#set username and password
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
client.loop_start()
client.connect(broker, port)      #connect to broker


def publish_To_Topic(topic, message):
	client.publish(topic,message)
	print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
	print ("")


#====================================================
# FAKE SENSOR 
# Dummy code used as Fake Sensor to publish some random values
# to MQTT Broker

toggle = 0

def publish_Fake_Sensor_Values_to_MQTT():
	threading.Timer(5.0, publish_Fake_Sensor_Values_to_MQTT).start()
	global toggle
	if toggle == 0:
		Humidity_Fake_Value = float("{0:.2f}".format(random.uniform(20, 100)))

		Humidity_Data = {}
		Humidity_Data['Sensor_ID'] = "Dummy-1"
		Humidity_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
		Humidity_Data['Humidity'] = Humidity_Fake_Value
		humidity_json_data = json.dumps(Humidity_Data)

		print ("Publishing fake Humidity Value: " + str(Humidity_Fake_Value) + "...")
		publish_To_Topic (MQTT_Topic_Humidity, humidity_json_data)
		toggle = 1

	else:
		Temprature_Fake_Value = float("{0:.2f}".format(random.uniform(1, 30)))

		Temprature_Data = {}
		Temprature_Data['Sensor_ID'] = "Dummy-2"
		Temprature_Data['Date'] = (datetime.today()).strftime("%d-%b-%Y %H:%M:%S:%f")
		Temprature_Data['Temprature'] = Temprature_Fake_Value
		Temprature_json_data = json.dumps(Temprature_Data)

		print ("Publishing fake Temprature Value: " + str(Temprature_Fake_Value) + "...")
		publish_To_Topic (MQTT_Topic_Temprature, Temprature_json_data)
		toggle = 0


while not client.connected_flag: #wait in loop
	print("Waiting for connection...")
	time.sleep(2)

try:
	publish_Fake_Sensor_Values_to_MQTT()


except KeyboardInterrupt:
	print ("Exiting....")
	client.disconnect()
	client.loop_stop()
#====================================================
