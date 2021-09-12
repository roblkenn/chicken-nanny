#!/usr/bin/env python

from datetime import timedelta
import datetime
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

doorOpenTime = sunriseTime
doorCloseTime = sunsetTime + timedelta(minutes=15)

print(f'Sunrise: {sunriseTime}')
print(f'Sunset: {sunsetTime}')
print(f'Door Open: {doorOpenTime.minute} {doorOpenTime.hour} * * *')
print(f'Door Close: {doorCloseTime.minute} {doorCloseTime.hour} * * *')

with CronTab(user='pi') as cron:
    cron.remove_all(comment='door')

    doorOpenJob = cron.new(comment='door', command=f'/home/pi/chicken-nanny/lights.py --on')
    doorOpenJob.setall(f'{doorOpenTime.minute} {doorOpenTime.hour} * * *')

    doorCloseJob = cron.new(comment='door', command=f'/home/pi/chicken-nanny/lights.py --off')
    doorCloseJob.setall(f'{doorCloseTime.minute} {doorCloseTime.hour} * * *')
