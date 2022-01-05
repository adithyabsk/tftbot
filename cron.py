#!/usr/bin/env python
"""Cron job for tweeting"""

import os
import random

from apscheduler.schedulers.blocking import BlockingScheduler
from dotenv import load_dotenv
from tzlocal import get_localzone

from tftbot import ObsidianTwitterBot, RoamTwitterBot

# Set random seed
random.seed(42)

# If a `.env` file exists, load in those environment variables
load_dotenv()

# Pull in required environment variables
# Twitter
twitter_consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
twitter_consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
twitter_access_token = os.environ["TWITTER_ACCESS_TOKEN"]
twitter_access_secret = os.environ["TWITTER_ACCESS_SECRET"]

# TFTChoice
tft_choice = os.environ["TFT_CHOICE"]

if tft_choice == "ROAM":
    roam_tag = os.environ["TAG"]
    roam_api_graph = os.environ["ROAM_API_GRAPH"]
    roam_api_email = os.environ["ROAM_API_EMAIL"]
    roam_api_password = os.environ["ROAM_API_PASSWORD"]

    tfttb = RoamTwitterBot(
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_secret,
        roam_tag,
        roam_api_graph,
        roam_api_email,
        roam_api_password,
    )
elif tft_choice == "OBSIDIAN":
    obsidian_tag = os.environ["TAG"]
    obsidian_vault_name = os.environ["OBSIDIAN_VAULT_NAME"]
    tfttb = ObsidianTwitterBot(
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_secret,
        obsidian_tag,
        obsidian_vault_name,
    )
else:
    raise ValueError("Undefined TFT_CHOICE")

# Immediately run a test tweet
tfttb.tweet_random_note()

# TODO: figure out handling custom timezones
# Create an instance of scheduler and add function
# Critical Note: on Heroku, cron does not work unless the job has an id, even though it is an optional parameter
scheduler = BlockingScheduler(timezone=get_localzone())
scheduler.add_job(
    tfttb.tweet_random_note, "cron", id="main_job", minute=5, hour=17
)  # 5:05pm GMT every day (12:05pm EST)
scheduler.add_job(
    tfttb.tweet_sponsor_request, "cron", id="sponsor_job", minute=1, hour=17, day=4
)  # 5:05pm once a month

scheduler.start()
