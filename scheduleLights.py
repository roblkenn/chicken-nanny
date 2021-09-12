#!/usr/bin/env python

from datetime import timedelta
from suntime import Sun
from crontab import CronTab

LATITUDE = 41.99
LONGITUDE = 83.43

sun = Sun(LATITUDE, -LONGITUDE)

sunriseTime = sun.get_local_sunrise_time()
sunsetTime = sun.get_local_sunset_time()

# Workaround for a crappy library
if sunsetTime < sunriseTime:
    sunsetTime = sunsetTime + timedelta(days=1)

lightsOnTime = sunsetTime - timedelta(minutes=15)
lightsOffTime = sunriseTime + timedelta(hours=14)
shouldUseLights = lightsOffTime > sunsetTime

print(f'Sunrise: {sunriseTime}')
print(f'Sunset: {sunsetTime}')
print(f'Lights On: {lightsOnTime}')
print(f'Lights Out: {lightsOffTime}')
print(f'Should Use Lights: {shouldUseLights}')

with CronTab(user='pi') as cron:
    cron.remove_all(comment='lights')

    if shouldUseLights:
        lightsOnJob = cron.new(comment='lights', command=f'python3 /home/pi/chicken-nanny/lights.py --on')
        lightsOnJob.setall(f'{lightsOnTime.minute} {lightsOnTime.hour} * * *')

        lightsOffJob = cron.new(comment='lights', command=f'python3 /home/pi/chicken-nanny/lights.py --off')
        lightsOffJob.setall(f'{lightsOffTime.minute} {lightsOffTime.hour} * * *')
