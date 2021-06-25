#!/usr/bin/env python

import click
import board
from adafruit_dotstar import DotStar

@click.command()
@click.option('--on/--off', required=True, default=True, help='Flag to turn lights on or off.')
def handleLights(on):
    click.echo('Turning On...' if on else 'Turning Off...')
    BRIGHTNESS = 1.0 if on else 0.0
    click.echo(f'Brightness: {BRIGHTNESS}')

    dots = DotStar(board.SCK, board.MOSI, 30, brightness=BRIGHTNESS)
    dots.fill((255, 255, 255))
    dots.show()
    click.echo('On' if on else 'Off')


if __name__ == '__main__':
    handleLights()