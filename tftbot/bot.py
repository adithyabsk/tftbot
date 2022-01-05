import random
import textwrap
import urllib.parse
from datetime import date

import tweepy
from dotenv import load_dotenv

from .obsidian import get_random_tag_block
from .roam import block_search

load_dotenv()

# Consts
MAX_TWEET = 240
MAX_NUM_TWEET = 9


class TFTTwitterBotMixin:
    """A Mixin class that provides the twitter bot functionality

    Tweets out strings out arbitrary length by splitting them up into separate
    tweets. Requires the `pick_random_block` method to be implemented.


    Parameters:
        twitter_consumer_key: The twitter application consumer key
        twitter_consumer_secret: The twitter application consumer secret
        twitter_access_token: The twitter oauth access token
        twitter_access_secret: The twitter oauth access secret
    """

    def __init__(
        self,
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_secret,
    ):
        # Setup twitter api client
        auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
        auth.set_access_token(twitter_access_token, twitter_access_secret)
        self.twitter_api = tweepy.API(auth)

    def pick_random_block(self):
        """Pick a random roam block from a list of collected blocks

        Returns:
            tuple[str, str]: the callback url and the block text
        """
        raise NotImplementedError("")

    # TODO: Maybe use nltk to tokenize so that thoughts are self contained in tweets. Do a little more
    #       digging to see if this is a solved problem; cursory searches indicate it is not.
    #       https://stackoverflow.com/a/4576110/3262054
    def split_tweet_msg(self, long_string, block_url):
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
        sponsor_url = "https://github.com/sponsors/adithyabsk?o=sd&sc=t"
        today = date.today().strftime("%B %d, %Y")
        sponsor_msg = f"It's {today}. Consider supporting this bot's creator @adithya_balaji\n\n{sponsor_url}"
        self.twitter_api.update_status(sponsor_msg)
        print("Sponsor Tweet posted")

    def tweet_random_note(self):
        # We use prints here because Heroku prints these to the the logs
        print("Collecting Roam Blocks...")
        block_url, block_text = self.pick_random_block()
        tweets = self.split_tweet_msg(block_text, block_url)
        self.compose_tweets(tweets)
        print("Roam Tweets posted")


class RoamTwitterBot(TFTTwitterBotMixin):
    """A Twitter Bot that tweets out a random note from a Roam Research Graph.

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

    def __init__(
        self,
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_secret,
        roam_tag,
        roam_api_graph,
        roam_api_email,
        roam_api_password,
    ):
        super().__init__(
            twitter_consumer_key,
            twitter_consumer_secret,
            twitter_access_token,
            twitter_access_secret,
        )
        # Set up roam variables
        self.roam_tag = roam_tag
        self.roam_api_graph = roam_api_graph
        self.roam_api_email = roam_api_email
        self.roam_api_password = roam_api_password

    # TODO: Maybe look into configurations for more intelligent heuristics for picking indexed roam blocks? Spaced
    #       repetition, etc...
    def pick_random_block(self):
        """Pick a random roam block from a list of roam blocks

        Returns:
            tuple[str, str]: the block id and the block text
        """
        options = block_search(
            self.roam_tag,
            self.roam_api_graph,
            self.roam_api_email,
            self.roam_api_password,
            max_length=MAX_TWEET * MAX_NUM_TWEET,
        )

        block_id, block_text = random.choice(options)
        block_url = (
            f"https://roamresearch.com/#/app/{self.roam_api_graph}/page/{block_id}"
        )

        return block_url, block_text


class ObsidianTwitterBot(TFTTwitterBotMixin):
    """A Twitter Bot that tweets out a random note from an Obsidian vault.

    Parameters:
        twitter_consumer_key: The twitter application consumer key
        twitter_consumer_secret: The twitter application consumer secret
        twitter_access_token: The twitter oauth access token
        twitter_access_secret: The twitter oauth access secret
        tag: The tag to search for in your obsidian vault
        vault_name: The of the obsidian vault
    """

    def __init__(
        self,
        twitter_consumer_key,
        twitter_consumer_secret,
        twitter_access_token,
        twitter_access_secret,
        tag,
        vault_name,
    ):
        super().__init__(
            twitter_consumer_key,
            twitter_consumer_secret,
            twitter_access_token,
            twitter_access_secret,
        )
        # Set up roam variables
        self.tag = tag
        self.vault_name = vault_name

    # TODO: Maybe look into configurations for more intelligent heuristics for picking indexed roam blocks? Spaced
    #       repetition, etc...
    def pick_random_block(self):
        """Pick a random roam block from a list of collected blocks

        Returns:
            tuple[str, str]: the block url and the block text
        """
        block_text = get_random_tag_block(self.tag)
        vault_name = urllib.parse.quote_plus(self.vault_name)
        search_str = " ".join(block_text.split(" ")[:10])
        search_str = search_str.replace('"', '\\"')
        query = urllib.parse.quote('"' + search_str + '"')
        # This does not work because twitter does not linkify URIs
        # block_url = f"obsidian://search?vault={vault_name}&query={query}"
        block_url = (
            f"https://www.adithyabalaji.com/obsidian/search/?vault={vault_name}"
            f"&query={query}"
        )

        return block_url, block_text
