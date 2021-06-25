#!/usr/bin/env python

import board
import click
from adafruit_ina219 import INA219
from busio import I2C
from gpiozero import Motor

@click.command()
@click.option('--open/--close', required=True, default=True, help='Flag to open of close door.')
def handleDoor(open):
    """Program that opens or closes the chicken door."""
    click.echo("Opening..." if open else "Closing...")

    motor = Motor(11, 13, 15, False)
    sensor = INA219(I2C(board.SCL, board.SDA))

    if open:
        motor.forward()
    else:
        motor.backward()

    handleStop(motor, sensor)

    click.echo("Opened" if open else "Closed")

def handleStop(motor, sensor):
    # TODO: Test motor ram amperage and adjust value below
    while sensor.current < 800:
        continue
    motor.stop()

if __name__ == '__main__':
    handleDoor()