import PySimpleGUI as sg
from libries.utils import *
from main import Main
from threading import Thread
import logging



sg.change_look_and_feel('DarkAmber')

#--------------------------------------LOGIN--------------------------------------------------------------------------
layout=[
    [sg.Text('Extrator de Questões', size=(100, 1), justification='center', font=("Helvetica", 20), relief=sg.RELIEF_RIDGE)],
    [sg.Text('', size=(15, 1), font=("Helvetica", 15))],
    [sg.Text('Link do Caderno de Questões:', size=(25,1), font=("Helvetica", 14))],
    [sg.In(size=(45,2), key=("link"))],
    [sg.Text('Quantiade de Questões:', size=(20, 0), font=("Helvetica", 14)), sg.In(size=(8,1), key=("pages"), default_text='50')],
    [sg.Radio('SHOW', "RADIO1", default=True, key=("task")), sg.Radio('OFF', "RADIO1", key=("task"))],
    [sg.Text('', size=(7,0))], 
    [sg.Text('Finalizado!', size=(30,1), font=("Helvetica", 15),  visible=False, key='-CBOX-')], 
    [sg.Text('', size=(7,0))], 
    [sg.Text('', size=(8,0)), sg.Button('INICIAR', border_width=5, size=(20, 1), key=("run")),sg.Button('Login', border_width=5, size=(10, 1), key=("login"))],
    [sg.Text('', size=(8,0)), sg.Button('Login Confirmar', border_width=5, size=(15, 1), key=("login_"), visible=False)], 
    [sg.Text('', size=(6,0)), sg.Output(size=(40,7))]
    ]


#--------------------------------------EXECUTION--------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(name)s %(levelname)s %(message)s',
    filename=f'./logs/log_{time_now("%Y-%m-%d %H-%M-%S")}.log',
    filemode='w')

log = logging.getLogger(__name__)
exe = Main()

window = sg.Window('Extrator de Questões', layout, size=(450, 450))

while True:
    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Cancelar'):
        break

    elif event == 'run':
        # exe.run(values['link'], int(values['pages']))
        Thread(target = exe.run, args = (values['link'], int(values['pages']))).start()

    elif event == 'login':
        window['login_'].Update(visible=True)
        exe.loginManual()

    elif event == 'login_':
        window['login_'].Update(visible=False)
        exe.close()

window.close()

