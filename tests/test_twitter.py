"""Unit tests for bot."""

import os

import pytest

RUN_INTEGRATION = bool(os.getenv("INTEGRATION", False))


def test_split_tweet_240():
    from tftbot.bot import TFTTwitterBotMixin

    li240 = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a convallis magna."

    random_id = "W9oV9twrW"
    rtb = TFTTwitterBotMixin(
        twitter_consumer_key="test",
        twitter_consumer_secret="test",
        twitter_access_token="test",
        twitter_access_secret="test",
    )
    assert li240 in rtb.split_tweet_msg(li240, random_id)[0]


def test_split_tweet_960():
    from tftbot.bot import TFTTwitterBotMixin

    li960 = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum id mollis magna. Phasellus quis mollis "
        "lacus, vel varius mauris. Nam ultricies ante eget auctor eleifend. Cras lobortis consectetur ipsum, sed "
        "commodo tortor. Sed hendrerit varius lobortis. Donec efficitur risus ac dapibus blandit. Vestibulum accumsan "
        "mollis tortor vitae rhoncus. Vivamus egestas sem id nunc pulvinar, sed condimentum lectus lobortis. Aliquam "
        "quis lectus eu nisi posuere dapibus id in leo. Suspendisse nec massa nec dolor feugiat tincidunt non non "
        "turpis. Donec eu scelerisque augue, posuere cursus eros. Sed non erat ut libero cursus tincidunt. Fusce "
        "eleifend auctor ullamcorper. Proin laoreet commodo metus ut tempus. Nulla vitae accumsan dolor.\n\n"
        "Ut ac diam magna. Aliquam eu pulvinar enim. Sed porta tellus nec placerat faucibus. Maecenas at laoreet diam, "
        "vel suscipit ligula. Proin egestas posuere aliquam. Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Proin et."
    )

    # this should be five because of the slippage from indicating the number of tweets in the thread
    random_id = "W9oV9twrW"
    rtb = TFTTwitterBotMixin(
        twitter_consumer_key="test",
        twitter_consumer_secret="test",
        twitter_access_token="test",
        twitter_access_secret="test",
    )
    assert len(rtb.split_tweet_msg(li960, random_id)) == 5


@pytest.mark.skipif(
    not RUN_INTEGRATION,
    reason=(
        "WARNING: Tweets out to live connected account. Requires twitter env "
        "vars to be configured. Runs for around 1s."
    ),
)
def test_integration_bot_tweet():
    """Tweet out a mocked out note from tweet_random_note."""
    from dotenv import load_dotenv

    from tftbot.bot import TFTTwitterBotMixin

    load_dotenv("../.env")

    twitter_consumer_key = os.environ["TWITTER_CONSUMER_KEY"]
    twitter_consumer_secret = os.environ["TWITTER_CONSUMER_SECRET"]
    twitter_access_token = os.environ["TWITTER_ACCESS_TOKEN"]
    twitter_access_secret = os.environ["TWITTER_ACCESS_SECRET"]

    rtb = TFTTwitterBotMixin(
        twitter_consumer_key=twitter_consumer_key,
        twitter_consumer_secret=twitter_consumer_secret,
        twitter_access_token=twitter_access_token,
        twitter_access_secret=twitter_access_secret,
    )

    rtb.compose_tweets(["Test Tweet."])
    rtb.tweet_sponsor_request()
