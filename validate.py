# validate.py
# Validate the model on a corpus of tweets scraped from Twitter.

# %%
# Imports
import pandas as pd
import tweepy as tw
import numpy as np
from os import environ as env
import streamlit as st
from transformers import pipeline

# %%
# Load credentials from .env file
auth = tw.AppAuthHandler(env["CONSUMER_KEY"], env["CONSUMER_SECRET"])

# Authorize
api = tw.API(auth)

# %%
# Get validation data (tweets) from Twitter
SCREEN_NAMES = []

MAX_TWEETS = 10

dfs_list = []
for name in SCREEN_NAMES:
    try:
        # Creation of query method using parameters
        tweets = tw.Cursor(
            api.user_timeline, screen_name=name, tweet_mode="extended"
        ).items(MAX_TWEETS)

        # Post-process tweets
        tweets_json = [t._json for t in tweets]
        tweets_normalized = pd.json_normalize(tweets_json)
        dfs_list.append(tweets_normalized)
    except:
        print("Unable to find tweets for {}".format(name))

# Combine all dfs into one df and clean
tweets_df = pd.concat(dfs_list)
tweets_df = tweets_df[
    ["created_at", "id", "full_text", "user.id_str", "user.name", "user.screen_name"]
]

# %%
# Classify tweets
classifier = pipeline("zero-shot-classification")
