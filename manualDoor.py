import os
from gpiozero import Button

def pollButton():
    button = Button(25)
    while True:
        button.wait_for_press()
        isOpen = getStatus()
        os.system(f"door.py --{'close' if isOpen else 'open'}")


def getStatus():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'doorStatus'), 'r') as f:
        status = f.read()
    return status == 'open'


pollButton()
