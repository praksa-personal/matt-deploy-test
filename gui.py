import PySimpleGUI as sg
from time import sleep

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
        [sg.ProgressBar(200, orientation='h', size=(50, 10), key='progressbar')],
     ]

window = sg.Window('MQTT connection test', layout, size=(340,300), grab_anywhere=True)

while True:
  event, values = window.read()   # Read the event that happened and the values dictionary
  
  if event == sg.WIN_CLOSED or event == 'Exit': 
    break
  if event == 'Start test':
    #print('You pressed the button')
    #print(values)
    window['Start test'].update(disabled=True,disabled_button_color = ("white","grey")) 

    for i in range(179):
      window['progressbar'].UpdateBar(i) 
      sleep(0.1) #on msg count




    #window['progressbar'].UpdateBar(200)  #on stop msg
window.close()