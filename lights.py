#!/usr/bin/env python

import board
import click
from adafruit_dotstar import DotStar

@click.command()
@click.option('--on/--off', required=True, default=True, help='Flag to turn lights on or off.')
def handleLights(on):
    print('Turning On...' if on else 'Turning Off...')
    BRIGHTNESS = 0.15 if on else 0.0
    print(f'Brightness: {BRIGHTNESS}')

    dots = DotStar(board.SCLK, board.MOSI, 60, brightness=BRIGHTNESS)
    dots.fill((255, 255, 255))
    dots.show()
    print('On' if on else 'Off')


if __name__ == '__main__':
    handleLights()
