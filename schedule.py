#!/usr/bin/env python

from datetime import timedelta, timezone
import datetime
from suntime import Sun
import os
import shlex
import subprocess

LATITUDE = 41.99
LONGITUDE = 83.43

sun = Sun(LATITUDE, -LONGITUDE)

# currentDate = datetime.datetime(2021, 12, 22)
currentDate = datetime.date.today()
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

currentTime = datetime.datetime.now(timezone.utc)

if shouldUseLights:
    lightsOnTime = sunsetTime - timedelta(minutes=30)

    if currentTime >= lightsOnTime and currentTime < lightsOffTime:
        os.system('/home/pi/chicken-nanny/lights.py --on')
    elif currentTime < lightsOnTime:
        lightsOnCommand = f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset -00:30 && /home/pi/chicken-nanny/lights.py --on'
        subprocess.Popen(shlex.split(lightsOnCommand), start_new_session=True)
    
    if currentTime >= lightsOffTime:
        os.system('/home/pi/chicken-nanny/lights.py --off')
    elif currentTime < lightsOffTime:
        lightsOffCommand = f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset {sunsetOffset.seconds//3600:02d}:{(sunsetOffset.seconds//60)%60:02d} && /home/pi/chicken-nanny/lights.py --off'
        subprocess.Popen(shlex.split(lightsOffTime), start_new_session=True)

doorCloseTime = sunsetTime + timedelta(minutes=15)

if currentTime >= sunriseTime and currentTime < doorCloseTime:
    os.system('/home/pi/chicken-nanny/door.py --be-free')
elif currentTime < sunriseTime:
    doorOpenCommand = f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunrise && /home/pi/chicken-nanny/door.py --be-free'
    subprocess.Popen(shlex.split(doorOpenCommand), start_new_session=True)

if currentTime >= doorCloseTime:
    os.system('/home/pi/chicken-nanny/door.py --close')
elif currentTime < doorCloseTime:
    doorCloseCommand = f'heliocron --latitude={LATITUDE}N --longitude={LONGITUDE}W wait --event sunset --offset 00:15 && /home/pi/chicken-nanny/door.py --close'
    subprocess.Popen(shlex.split(doorCloseCommand), start_new_session=True)
