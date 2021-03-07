"""Cron job for tweeting"""

from tzlocal import get_localzone
from apscheduler.schedulers.blocking import BlockingScheduler

from bot import main, sponsor_tweet

# TODO: figure out handling custom timezones
# Create an instance of scheduler and add function
# Critical Note: on Heroku, cron does not work unless the job has an id, even though it is an optional paramter
scheduler = BlockingScheduler(timezone=get_localzone())
scheduler.add_job(main, "cron", id="main_job", minute=5, hour=17)  # 5:05pm every day
scheduler.add_job(sponsor_tweet, "cron", id="sponsor_job", minute=1, hour=17, day=4)  # 5:05pm once a month

scheduler.start()
