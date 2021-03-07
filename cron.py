#!/usr/bin/env python
"""Cron job for tweeting"""

import os

from tzlocal import get_localzone
from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv

from roambot import RoamTwitterBot

# If a `.env` file exists, load in those environment variables
load_dotenv()

# Pull in required environment variables
# Roam
roam_tag = os.environ["ROAM_TAG"]
roam_api_graph = os.environ["ROAM_API_GRAPH"]
roam_api_email = os.environ["ROAM_API_EMAIL"]
roam_api_password = os.environ["ROAM_API_PASSWORD"]
# Twitter
twitter_consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
twitter_consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
twitter_access_token = os.environ["TWITTER_ACCESS_TOKEN"]
twitter_access_secret = os.environ["TWITTER_ACCESS_SECRET"]

# Initialize roam twitter bot only after environment variables have been set
rtb = RoamTwitterBot(
    roam_tag, roam_api_graph, roam_api_email, roam_api_password, twitter_consumer_key,
    twitter_consumer_secret, twitter_access_token, twitter_access_secret
)

# TODO: figure out handling custom timezones
# Create an instance of scheduler and add function
# Critical Note: on Heroku, cron does not work unless the job has an id, even though it is an optional parameter
scheduler = BlockingScheduler(timezone=get_localzone())
scheduler.add_job(rtb.tweet_roam_note, "cron", id="main_job", minute=5, hour=17)  # 5:05pm GMT every day (12:05pm EST)
scheduler.add_job(rtb.tweet_sponsor_request, "cron", id="sponsor_job", minute=1, hour=17, day=4)  # 5:05pm once a month

scheduler.start()
