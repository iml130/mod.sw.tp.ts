import paho.mqtt.client as mqtt
import time

acttim = 0
psent = 0
link = "Online"
switchVal = 0

def on_connect(client, userdata, flags, rc):
	global link
	client.publish("/123456789/l4ms/san_1/attrs/link",link)
	
def stat():
	global acttim, psent, switchVal

	prec = psent
	msg = str(acttim)+"	"+str(54)+"	"+str(psent)+"	"+str(prec)+"	"
	client.publish("/123456789/l4ms/san_1/attrs/stat",msg)
	client.publish("/123456789/l4ms/san_1/attrs/sw",switchVal)
	acttim+=60
	psent+=1
	switchVal+=1
	if(switchVal == 4):
		switchVal = 0

	time.sleep(60)

client = mqtt.Client()
client.on_connect = on_connect
client.connect("192.168.0.110", 1883, 60)
client.loop_start()

while True:
	stat()
	time.sleep(1)
