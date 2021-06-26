import os
from gpiozero import Button

dir_path = os.path.dirname(os.path.realpath(__file__))

def pollButton():
    button = Button(25)
    while True:
        button.wait_for_press()
        isOpen = getStatus()
        scriptPath = os.path.join(dir_path, 'door.py')
        os.system(f"{scriptPath} --{'close' if isOpen else 'open'}")


def getStatus():
    with open(os.path.join(dir_path, 'doorStatus'), 'r') as f:
        status = f.read()
    return status == 'open'


pollButton()
