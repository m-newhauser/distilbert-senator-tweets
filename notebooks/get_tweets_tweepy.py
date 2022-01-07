# build_dataset.py

# %%
# Imports
import datetime
from datetime import datetime
import pytz
import pandas as pd
import tweepy as tw
import numpy as np
import preprocessor as p
from os import environ as env

# %%
MIN_DATE = Timestamp("2021-01-01 00:00:00+0000")

# %%
# Read in senator usernames and parties
usernames_df = pd.read_csv("data/senators_usernames.csv")
usernames_list = usernames_df.username.tolist()[0:5]

# %%
# Load credentials from .env file and authorize
auth = tw.AppAuthHandler(env["CONSUMER_KEY"], env["CONSUMER_SECRET"])
api = tw.API(auth)

# %%
# Get raw tweets
dfs_list = []
failed_list = []

for name in usernames_list:
    try:
        # Send a query
        tweets = api.user_timeline(screen_name=name, tweet_mode="extended", count=200)

        # Post-process tweets
        tweets_json = [t._json for t in tweets]
        tweets_normalized = pd.json_normalize(tweets_json)
        dfs_list.append(tweets_normalized)
    except:
        print("Unable to find tweets for {}".format(name))
        failed_list.append(name)

#%%
# Combine all dfs into one df and clean
tweets_raw_df = pd.concat(dfs_list)

# Clean data
tweets_df = (
    tweets_raw_df.filter(["created_at", "id", "full_text", "user.screen_name"])
    .assign(
        text_clean=tweets_raw_df["full_text"]
        .apply(p.clean)
        .str.replace("&amp;", "and ")
        .str[:512],  # remove &'s and truncate
        created_at=lambda x: pd.to_datetime(
            tweets_raw_df["created_at"],
        ),
    )
    .rename(columns={"user.screen_name": "username"})
    .query(f"created_at >= {MIN_DATE}")
)

# # Convert date column
# tweets_df["timestamp"] = list(map(lambda x: datetime.strptime(x,'%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d %H:%M:%S'), tweets_df['created_at']))

# # %%
# tweets_df.groupby("username").agg(Minimum_Date=('created_at', np.min), Maximum_Date=('created_at', np.max), count=('created_at', len))
# %%
