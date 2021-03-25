"""End to end integration test."""

import os

import pytest


@pytest.mark.skipif(os.getenv("INTEGRATION", False) is False,
                    reason=(
                            "WARNING: Tweets out to live connected account. Requires all env "
                            "vars to be configured. Runs for around 10s."
                    ))
def test_integration_end_to_end_roam():
    """Tweet out a mocked out note from tweet_roam_note."""
    from dotenv import load_dotenv

    from roambot.bot import RoamTwitterBot

    load_dotenv("../.env")

    roam_tag = os.environ["ROAM_TAG"]
    roam_api_graph = os.environ["ROAM_API_GRAPH"]
    roam_api_email = os.environ["ROAM_API_EMAIL"]
    roam_api_password = os.environ["ROAM_API_PASSWORD"]
    twitter_consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    twitter_consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    twitter_access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    twitter_access_secret = os.environ["TWITTER_ACCESS_SECRET"]

    rtb = RoamTwitterBot(
        roam_tag, roam_api_graph, roam_api_email, roam_api_password,
        twitter_consumer_key, twitter_consumer_secret, twitter_access_token, twitter_access_secret
    )

    rtb.tweet_roam_note()
    rtb.tweet_sponsor_request()
