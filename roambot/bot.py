import os
import random
import textwrap

import tweepy
from dotenv import load_dotenv

from .roam import block_search

load_dotenv()

# Consts
MAX_TWEET = 240
MAX_NUM_TWEET = 9
SPONSOR_URL = "https://github.com/sponsors/adithyabsk?o=sd&sc=t"
SPONSOR_MSG = f"Consider supporting this bot's creator @adithya_balaji\n\n{SPONSOR_URL}"


class RoamTwitterBot:
    """A Twitter Bot that periodically tweets out selected notes from a Roam Research Graph.

    Note:
        For information about properly setting the roam related variables please see:
        For information about the twitter api keys please see:


    Parameters:
        roam_tag: The tag to search for in your roam graph
        roam_api_graph: The name of your Roam graph
        roam_api_email: The email used to register for Roam Research
        roam_api_password: The password for your Roam Research account
        twitter_consumer_key: The twitter application consumer key
        twitter_consumer_secret: The twitter application consumer secret
        twitter_access_token: The twitter oauth access token
        twitter_access_secret: The twitter oauth access secret

    """

    def __init__(self, roam_tag, roam_api_graph, roam_api_email, roam_api_password,
                 twitter_consumer_key, twitter_consumer_secret, twitter_access_token,
                 twitter_access_secret):
        # Set up roam variables
        self.roam_tag = roam_tag
        self.roam_api_graph = roam_api_graph
        self.roam_api_email = roam_api_email
        self.roam_api_password = roam_api_password

        # Setup twitter api client
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token, twitter_access_secret)
        self.twitter_api = tweepy.API(auth)

    # TODO: Maybe look into configurations for more intelligent heuristics for picking indexed roam blocks? Spaced
    #       repetition, etc...
    def pick_roam_block(self):
        """Pick a random roam block from a list of roam blocks

        Returns:
            tuple[str, str]: the block id and the block text

        """
        options = block_search(
            self.roam_tag,
            self.roam_api_graph,
            self.roam_api_email,
            self.roam_api_password,
            max_length=MAX_TWEET * MAX_NUM_TWEET)

        return random.choice(options)

    # TODO: Maybe use nltk to tokenize so that thoughts are self contained in tweets. Do a little more
    #       digging to see if this is a solved problem; cursory searches indicate it is not.
    #       https://stackoverflow.com/a/4576110/3262054
    def split_tweet_msg(self, long_string, block_id):
        block_url = f"https://roamresearch.com/#/app/{self.roam_api_graph}/page/{block_id}"
        template_tweet = f"{long_string}\n\n{block_url}"
        if len(template_tweet) <= MAX_TWEET:
            return [template_tweet]
        else:
            # Should only be 6 characters max since max number of tweets is 9. This is a hacky limit
            # so that I don't have to handle the case where I am not "maximally tweeting". (Note we add
            # a newline character to make it six
            thread_indicator = "\n\n({}/{})"
            ind_len = 7
            snippets = textwrap.wrap(template_tweet, MAX_TWEET - ind_len)
            return [
                tweet + thread_indicator.format(i, len(snippets))
                for i, tweet in enumerate(snippets, 1)
            ]

    # TODO: Setup a way to directly link to roam block from tweet
    #       https://www.reddit.com/r/RoamResearch/comments/gfrois/links_to_blocks_pages_inside_roam_from_outside/fpwavnr/
    def compose_tweets(self, tweet_list):
        if len(tweet_list) == 0:
            raise ValueError("tweet_list cannot be empty.")
        else:
            prev_tweet = None
            for tweet_msg in tweet_list:
                if prev_tweet is None:
                    prev_tweet = self.twitter_api.update_status(tweet_msg)
                else:
                    prev_tweet = self.twitter_api.update_status(
                        tweet_msg,
                        in_reply_to_status_id=prev_tweet.id,
                        auto_populate_reply_metadata=True,
                    )

    def tweet_sponsor_request(self):
        print("Posting Sponsor Tweet")
        self.twitter_api.update_status(SPONSOR_MSG)
        print("Sponsor Tweet posted")

    def tweet_roam_note(self):
        # We use prints here because Heroku prints these to the the logs
        print("Collecting Roam Blocks...")
        block_id, block_text = self.pick_roam_block()
        tweets = self.split_tweet_msg(block_text, block_id)
        self.compose_tweets(tweets)
        print("Roam Tweets posted")
