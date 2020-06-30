import paho.mqtt.client as mqtt
import time

Msg = ' '  

def on_message(client, userdata, msg):
	if msg.topic == '/123456789/l4ms/san_1/attrs/stat':
		globMsg = msg.payload
		splitMsg = globMsg.split('	')
		Msg = splitMsg[0]
		client.publish("/1234/san_1_switch/attrs/acttim",Msg)
		Msg = splitMsg[2]
		client.publish("/1234/san_1_switch/attrs/psent",Msg)
		Msg = splitMsg[3]
		client.publish("/1234/san_1_switch/attrs/prec",Msg)
		
	elif msg.topic == '/123456789/l4ms/san_1/attrs/sw':
		globMsg = msg.payload
		client.publish("/1234/san_1_switch/attrs/sw",globMsg)
		
	elif msg.topic == '/123456789/l4ms/san_1/attrs/link':
		globMsg = msg.payload
		client.publish("/1234/san_1_switch/attrs/link",globMsg)
			
def on_disconnect(client, userdata,rc=0):
    logging.debug("DisConnected result code "+str(rc))
    client.loop_stop()

client = mqtt.Client()
client.on_message = on_message
client.connect("192.168.0.110", 1883, 60)

client.loop_start()
client.subscribe("/123456789/l4ms/#")

while True: 
	time.sleep(1)

	


