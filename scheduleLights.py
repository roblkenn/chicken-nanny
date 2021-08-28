#!/usr/bin/env python

from datetime import timedelta, timezone
import datetime
from suntime import Sun
from crontab import CronTab

LATITUDE = 41.99
LONGITUDE = 83.43

sun = Sun(LATITUDE, -LONGITUDE)

# currentDate = datetime.datetime(2021, 12, 22)
currentDate = datetime.date.today()
sunriseTime = sun.get_local_sunrise_time(currentDate)
sunsetTime = sun.get_local_sunset_time(currentDate)

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

utc_dt = datetime.datetime.now(timezone.utc)
currentTime = utc_dt.astimezone()
print(f'Current Time: {currentTime}')

if shouldUseLights:
    with CronTab(user='pi') as cron:
        cron.remove_all(comment='lights')

        lightsOnJob = cron.new(comment='lights', command=f'heliocron --latitude {LATITUDE}N --longitude {LONGITUDE}W wait --event sunset --offset -00:30 && /home/pi/chicken-nanny/lights.py --on')
        lightsOnJob.setall('0 15 * * *')

        lightsOffJob = cron.new(comment='lights', command=f'heliocron --latitude {LATITUDE}N --longitude {LONGITUDE}W wait --event sunset --offset {sunsetOffset.seconds//3600:02d}:{(sunsetOffset.seconds//60)%60:02d} && /home/pi/chicken-nanny/lights.py --off')
        lightsOffJob.setall('0 15 * * *')
