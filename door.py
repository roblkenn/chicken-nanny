#!/usr/bin/env python

import board
import click
import digitalio
from adafruit_ina219 import INA219
from busio import I2C
from time import sleep
import os

class Motor:
    def __init__(self, forwardPin, backwardPin):
        self.forwardPin = digitalio.DigitalInOut(forwardPin)
        self.backwardPin = digitalio.DigitalInOut(backwardPin)
        self.forwardPin.direction = digitalio.Direction.OUTPUT
        self.backwardPin.direction = digitalio.Direction.OUTPUT
        self.forwardPin.value = False
        self.backwardPin.value = False

    def forward(self):
        self.forwardPin.value = True
        self.backwardPin.value = False

    def backward(self):
        self.forwardPin.value = False
        self.backwardPin.value = True

    def stop(self):
        self.forwardPin.value = False
        self.backwardPin.value = False

@click.command()
@click.option('--be-free/--close', required=True, default=True, help='Flag to open of close door.')
def handleDoor(be_free):
    """Program that opens or closes the chicken door."""
    doorMotor = Motor(board.D21, board.D20)
    sensor = INA219(I2C(board.SCL, board.SDA))

    if be_free:
        doorMotor.forward()
    else:
        doorMotor.backward()

    handleStop(doorMotor, sensor)
    updateStatus(be_free)

def handleStop(doorMotor, sensor):
    sleep(0.5)
    while abs(sensor.current) < 500:
        continue
    doorMotor.stop()

def updateStatus(be_free):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dir_path, 'doorStatus')
    with open(filepath, 'w') as f:
        f.write('open' if be_free else 'closed')


if __name__ == '__main__':
    handleDoor()
