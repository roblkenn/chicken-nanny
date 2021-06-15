#!/usr/bin/env python

from datetime import timedelta
from suntime import Sun
import os

LATITUDE = 41.993822
LONGITUDE = -83.432436

sun = Sun(LATITUDE, LONGITUDE)

lightsOffTime = sun.get_local_sunrise_time() + timedelta(hours=15)
shouldUseLights = lightsOffTime <= sun.get_local_sunset_time()
sunsetOffset = lightsOffTime - sun.get_local_sunset_time()

print(f'Sunrise: {sun.get_local_sunrise_time()}')
print(f'Sunset: {sun.get_local_sunset_time()}')
print(f'Lights Out: {lightsOffTime}')
print(f'Should Use Lights: {shouldUseLights}')
print(f'Offset from Sunset: {sunsetOffset}')

if shouldUseLights:
    os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset -01:00 && /home/pi/chicken-nanny/lights.py --on')
    os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset 01:00 && /home/pi/chicken-nanny/lights.py --off');

os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunrise && /home/pi/chicken-nanny/door.py --open')
os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset 00:45 && /home/pi/chicken-nanny/door.py --close')
