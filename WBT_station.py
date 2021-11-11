import paho.mqtt.client as paho
import json
from time import sleep


def on_publish(client, userdata, mid):
    print("msg.id: "+str(mid))


data = {
    "user": "puntaric",
    "id": "XY123",
    "test_id": "TID123",
    "test_status": "OK",
    "finished": 0
}

data_json = json.dumps(data)

host_ip = "localhost"
this_client_id = ""


client = paho.Client(
                     clean_session=True, protocol=paho.MQTTv31)

client._username = "wbt"
client._password = "1234"

client.on_publish = on_publish
client.will_set("deploy/lastwill", this_client_id +
                " Gone Offline", qos=1, retain=False)


client.connect(host=host_ip, port=1883)
client.loop_start()

for i in range(60):
    (rc, mid) = client.publish("deploy/topic-1", str(data_json), qos=1)
    (rc, mid) = client.publish("deploy/topic-2", str(data_json), qos=1)
    (rc, mid) = client.publish("deploy/topic-3", str(data_json), qos=1)
    sleep(0.5)

for i in range(19):
    (rc, mid) = client.publish("deploy/topic-1", str(data_json), qos=1)
    sleep(0.5)

sleep(5)
(rc, mid) = client.publish("deploy/stop", "STOP", qos=1)

client.loop_stop()
