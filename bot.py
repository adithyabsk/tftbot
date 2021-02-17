import os
import random
import textwrap

import tweepy
from dotenv import load_dotenv

from roam import block_search

load_dotenv()

# Consts
MAX_TWEET = 240
MAX_NUM_TWEET = 9
# TODO: convert this to GH sponsors
SPONSOR_MSG = (
    "Consider supporting this bot's creator @adithya_balaji"
)

# env vars
ROAM_TAG = os.environ["ROAM_TAG"]
_TWITTER_CONSUMER_KEY = os.environ["TWITTER_CONSUMER_KEY"]
_TWITTER_CONSUMER_SECRET = os.environ["TWITTER_CONSUMER_SECRET"]
_TWITTER_ACCESS_TOKEN = os.environ["TWITTER_ACCESS_TOKEN"]
_TWITTER_ACCESS_SECRET = os.environ["TWITTER_ACCESS_SECRET"]

# Twitter API
_AUTH = tweepy.OAuthHandler(_TWITTER_CONSUMER_KEY, _TWITTER_CONSUMER_SECRET)
_AUTH.set_access_token(_TWITTER_ACCESS_TOKEN, _TWITTER_ACCESS_SECRET)
TWITTER_API = tweepy.API(_AUTH)


def pick_roam_block():
    options = block_search(ROAM_TAG, max_length=MAX_TWEET * MAX_NUM_TWEET)

    return random.choice(options)


# TODO: Maybe use nltk to tokenize so that thoughts are self contained in tweets. Do a little more
#       digging to see if this is a solved problem; cursory searches indicate it is not.
#       https://stackoverflow.com/a/4576110/3262054
def split_tweet_msg(long_string):
    if len(long_string) <= MAX_TWEET:
        return [long_string]
    else:
        # Should only be 6 characters max since max number of tweets in 9. This is a hacky limit
        # so that I don't have to handle the case where I am not "maximally tweeting". (Note we add
        # a newline character to make it six
        thread_indicator = "\n\n({}/{})"
        ind_len = 7
        snippets = textwrap.wrap(long_string, MAX_TWEET - ind_len)
        return [
            tweet + thread_indicator.format(i, len(snippets))
            for i, tweet in enumerate(snippets, 1)
        ]


# TODO setup a way to directly link to roam block from tweet
# https://www.reddit.com/r/RoamResearch/comments/gfrois/links_to_blocks_pages_inside_roam_from_outside/fpwavnr/
def compose_tweets(api, tweet_list):
    if len(tweet_list) == 0:
        raise ValueError("tweet_list cannot be empty.")
    else:
        prev_tweet = None
        for tweet_msg in tweet_list:
            if prev_tweet is None:
                prev_tweet = api.update_status(tweet_msg)
            else:
                prev_tweet = api.update_status(
                    tweet_msg,
                    in_reply_to_status_id=prev_tweet.id,
                    auto_populate_reply_metadata=True,
                )


def sponsor_tweet():
    print("Posting Sponsor Tweet")
    TWITTER_API.update_status(SPONSOR_MSG)
    print("Sponsor Tweet posted")


def main():
    print("Collecting Roam Blocks...")
    block = pick_roam_block()
    tweets = split_tweet_msg(block)
    compose_tweets(TWITTER_API, tweets)
    print("Roam Tweets posted")


if __name__ == "__main__":
    main()
