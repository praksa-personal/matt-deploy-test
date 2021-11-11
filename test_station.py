from time import sleep
import paho.mqtt.client as paho


def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed: "+str(mid)+" "+str(granted_qos))

def on_publish(client, userdata, mid):
    print("msg.id: "+str(mid))

def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.qos)+" "+str(msg.payload))
    global msg_count 
    msg_count += 1
    stop_check(msg)

def stop_check(msg):
    if(msg.topic == "deploy/stop"):
        if(msg.payload == b'STOP'):
            global rec_flag
            rec_flag = 0

host_ip = "localhost" #set to broker ip
print("Enter test station ID: ")
this_client_id = "Test-station-" + input()

msg_count = 0

client = paho.Client(client_id=this_client_id,
                     clean_session=False, protocol=paho.MQTTv31)
    
client.will_set("deploy/lastwill", this_client_id+ " Gone Offline",qos=1,retain=False)

client.on_subscribe = on_subscribe
client.on_message = on_message

client.connect(host=host_ip, port=1883)
client.subscribe("deploy/topic-1", qos=1)
client.subscribe("deploy/topic-2", qos=1)
client.subscribe("deploy/topic-3", qos=1)
client.subscribe("deploy/stop", qos=1)

client.loop_start()

rec_flag = 1

while(rec_flag):
    ()

(rc, mid) = client.publish("deploy/log", str("STOP, test finished, messages received on deploy/topic: " + str(msg_count)), qos=1)
sleep(2)


client.loop_stop()

