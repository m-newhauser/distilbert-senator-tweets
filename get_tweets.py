# %%
import pandas as pd
import tweepy as tw
from os import environ as env

# %%
# Load credentials from .env file
auth = tw.AppAuthHandler(env["CONSUMER_KEY"], env["CONSUMER_SECRET"])

# Authorize
api = tw.API(auth)

# %%
# Run a test query
username = "cathymcmorris"
max_tweets = 150

# Creation of query method using parameters
tweets = tw.Cursor(api.user_timeline, id=username, tweet_mode="extended").items(
    max_tweets
)

# %%
# Post-process tweets
json_tweets = [t._json for t in tweets]
tweets_df = pd.json_normalize(json_tweets)
tweets_df[
    [
        "created_at",
        "id",
        "full_text",
        "retweet_count",
        "favorite_count",
        "retweeted",
        "user.id_str",
        "user.name",
        "user.screen_name",
        "user.location",
        "user.url",
    ]
]
# %%
tweets_df.head()
