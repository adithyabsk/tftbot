"""Unit tests for bot."""


def test_split_tweet_240():
    from bot import split_tweet_msg

    li240 = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam a convallis magna. Pellentesque a nisl pharet"
        "ra, ornare est vel, ullamcorper diam. Pellentesque habitant morbi tristique senectus et netus et malesuada fam"
        "es ac turpis ligula."
    )

    assert li240 == split_tweet_msg(li240)[0]


def test_split_tweet_960():
    from bot import split_tweet_msg

    li960 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum id mollis magna. Phasellus quis mollis lacus, vel varius mauris. Nam ultricies ante eget auctor eleifend. Cras lobortis consectetur ipsum, sed commodo tortor. Sed hendrerit varius lobortis. Donec efficitur risus ac dapibus blandit. Vestibulum accumsan mollis tortor vitae rhoncus. Vivamus egestas sem id nunc pulvinar, sed condimentum lectus lobortis. Aliquam quis lectus eu nisi posuere dapibus id in leo. Suspendisse nec massa nec dolor feugiat tincidunt non non turpis. Donec eu scelerisque augue, posuere cursus eros. Sed non erat ut libero cursus tincidunt. Fusce eleifend auctor ullamcorper. Proin laoreet commodo metus ut tempus. Nulla vitae accumsan dolor.

Ut ac diam magna. Aliquam eu pulvinar enim. Sed porta tellus nec placerat faucibus. Maecenas at laoreet diam, vel suscipit ligula. Proin egestas posuere aliquam. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin et.
"""

    # this should be five because of the slippage from indicating the number of tweets in the thread
    assert len(split_tweet_msg(li960)) == 5
