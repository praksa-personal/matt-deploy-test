import PySimpleGUI as sg
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
    global window
    window['progressbar'].UpdateBar(msg_count) 
    stop_check(msg)

def stop_check(msg):
    if(msg.topic == "deploy/stop"):
        if(msg.payload == b'STOP'):
            global rec_flag
            rec_flag = 0


sg.theme('DarkAmber')  
layout = [ 
        [sg.Text('Broker IP')], # 0
        [sg.Input()],
        [sg.Text('Tst Client ID')], # 1
        [sg.Input()],
        [sg.Text('User')], # 2
        [sg.Input()],
        [sg.Text('Password')], # 3
        [sg.Input(password_char='*')],
        [sg.Button('Start test')],
        [sg.ProgressBar(220, orientation='h', size=(50, 10), key='progressbar')],
     ]
window = sg.Window('MQTT connection test', layout, size=(340,300), grab_anywhere=True)

##MQTT
msg_count = 0

while True:
  event, values = window.read()   # Read the event that happened and the values dictionary
  
  if event == sg.WIN_CLOSED or event == 'Exit': 
    break
  if event == 'Start test':
    host_ip = values[0]
    this_client_id = values[1]
    window['Start test'].update(disabled=True,disabled_button_color = ("white","grey")) 
    event, values = window.read(timeout=1)

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
      event, values = window.read(timeout=1)
      ()

    sleep(1)
    while(1):
      event, values = window.read(timeout=1)
      (rc, mid) = client.publish("deploy/log", str("STOP, test finished, messages received on deploy/topic: " + str(msg_count)), qos=1)
      sleep(5)
      window['progressbar'].UpdateBar(220) 
      client.loop_stop() 
      sleep(2)
      break

window.close()

