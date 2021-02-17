"""Cron job for tweeting"""

from tzlocal import get_localzone

from apscheduler.schedulers.blocking import BlockingScheduler

from bot import main, sponsor_tweet

# TODO: figure out handling custom timezones
# Create an instance of scheduler and add function
scheduler = BlockingScheduler(timezone=get_localzone())
scheduler.add_job(main, "cron", minute=5)  # , hour=17)  # 5:05pm server time
scheduler.add_job(sponsor_tweet, "cron", minute=5)  # , hour=17, day=4)  # 5:05pm once a month

scheduler.start()
