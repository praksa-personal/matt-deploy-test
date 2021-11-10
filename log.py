from time import sleep
import paho.mqtt.client as paho
from datetime import datetime

def on_subscribe(client, userdata, mid, granted_qos):
    t = datetime.now().strftime("%H:%M:%S")
    print("Subscribed: "+str(mid)+" "+str(granted_qos))
    global f
    f.write("\n" + t + " Subscribed: "+str(mid)+" "+str(granted_qos))

def on_message(client, userdata, msg):
    t = datetime.now().strftime("%H:%M:%S")
    print(msg.topic+" "+str(msg.qos)+" "+ str(msg.payload))
    global f
    f.write("\n" + t + " " + msg.topic+" "+str(msg.qos) + "\t" + str(msg.payload))


now = datetime.now()
dt_string = now.strftime("%H_%M_%S")
f = open("log_"+dt_string+".txt", "w")

host_ip = "localhost" #set to broker ip
this_client_id = "Log-client" 

client = paho.Client(client_id=this_client_id,
                     clean_session=False, protocol=paho.MQTTv31)
        
client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect(host=host_ip, port=1883)
client.subscribe("deploy/lastwill", qos=1)
client.subscribe("deploy/log", qos=1)
client.subscribe("deploy/stop", qos=1)

client.loop_start()

sleep(0.5)
print("Press any key to stop logging")
input()

client.disconnect()

t = datetime.now().strftime("%H:%M:%S")
f.write("\n\n" + t + " LOG END")
f.close()
