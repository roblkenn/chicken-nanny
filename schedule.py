#!/usr/bin/env python

from datetime import timedelta
import datetime
from suntime import Sun
import os

LATITUDE = 41.993822
LONGITUDE = -83.432436

sun = Sun(LATITUDE, LONGITUDE)

currentDate = datetime.datetime(2021, 12, 22)
sunriseTime = sun.get_sunrise_time(currentDate)
sunsetTime = sun.get_sunset_time(currentDate)

# Workaround for a crappy library
if sunsetTime < sunriseTime:
    sunsetTime = sunsetTime + timedelta(days=1)

lightsOffTime = sunriseTime + timedelta(hours=14)
shouldUseLights = lightsOffTime > sunsetTime
sunsetOffset = lightsOffTime - sunsetTime

print(f'Sunrise: {sunriseTime}')
print(f'Sunset: {sunsetTime}')
print(f'Lights Out: {lightsOffTime}')
print(f'Should Use Lights: {shouldUseLights}')
print(f'Offset from Sunset: {sunsetOffset}')
print(f'Offset formatted for heliocron: {sunsetOffset.seconds//3600:02d}:{(sunsetOffset.seconds//60)%60:02d}')

if shouldUseLights:
    os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset -00:30 && /home/pi/chicken-nanny/lights.py --on')
    os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset {sunsetOffset.seconds//3600:02d}:{(sunsetOffset.seconds//60)%60:02d} && /home/pi/chicken-nanny/lights.py --off');

#os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunrise && /home/pi/chicken-nanny/door.py --open')
os.system(f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset 00:15 && /home/pi/chicken-nanny/door.py --close')
