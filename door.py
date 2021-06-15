#!/usr/bin/env python

from gpiozero import Motor
import click
from time import sleep

@click.command()
@click.option('--open/--close', required=True, default=True, help='Flag to open of close door.')
def handleDoor(open):
    """Program that opens or closes the chicken door."""
    click.echo("Opening..." if open else "Closing...")

    motor = Motor(11, 13, 15, False)

    if open:
        motor.forward()
    else:
        motor.backward()

    handleStop(motor)

    click.echo("Opened" if open else "Closed")

def handleStop(motor):
    TIME_TO_RUN = 2
    sleep(TIME_TO_RUN)
    motor.stop()

if __name__ == '__main__':
    handleDoor()