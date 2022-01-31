#%%
from datetime import datetime
import pandas as pd
import snscrape
import sqlite3
from snscrape.modules import twitter
from sqlalchemy import create_engine

# %%
# Params
DATETIME_FORMAT = "%Y-%m-%d %I:%M:%S %p"

# START_DATE = "2021-01-20"  # YYYY-MM-DD
# END_DATE = "2021-12-31"  # YYYY-MM-DD

# %%
# Read in list of senator usernames
usernames = pd.read_csv(
    "/Users/mnewhauser/python-work/rep-or-dem-tweets/data/senators_usernames.csv"
)

# %%
# # Convert date strings for later pd.query()
# START_DATE = START_DATE.replace("-", "")
# END_DATE = END_DATE.replace("-", "")

#%%
def extract_tweets(scraped_profile):
    return [
        {
            "date": tweet.date.strftime(DATETIME_FORMAT),
            "id": tweet.id,
            "username": tweet.user.username,
            "text": tweet.content,
            "is_retweet": str(tweet.retweetedTweet),
        }
        for tweet in scraped_profile
    ]


def tidy_tweets(tweets):
    # Put tweet data into a df
    tweets_df = pd.DataFrame(tweets)
    # Tidy up
    return (
        tweets_df.query('is_retweet == "None"')  # remove all retweets
        .assign(date=pd.to_datetime(tweets_df.date))  # convert col from str to datetime
        # .query(f"{START_DATE} < date < {END_DATE}")  # drop tweets outside of date range
        .drop(columns=["is_retweet"])  # drop col
        .merge(usernames[["username", "party"]])
        .sort_values(by=["date"])  # sort by date
        .reset_index(drop=True)
    )


# %%
# Connect to locally created db (and create if it doesn't exist)
conn = sqlite3.connect(
    "/Users/mnewhauser/python-work/rep-or-dem-tweets/data/TWEETS.db"
)  # Command palette > SQLite: Open database

#%%
# Initalize empty list
dfs = []

# Get tweets by username and append to db
for username in usernames.username.tolist():
    try:
        # Get all tweets for given username
        scraped_profile = twitter.TwitterProfileScraper(username=username).get_items()
        # Extra tweet metadata
        tweets = extract_tweets(scraped_profile)
        # Tidy up tweets and put in df
        tweets_df = tidy_tweets(tweets)
        # Append to list
        dfs.append(tweets_df)
    except:
        print(f"Couldn't get tweets for {username}")

#%%
# Write df to senators table in Tweets db
for df in dfs:
    df.to_sql("senators", conn, if_exists="replace", chunksize=10000)

# %%
# Close connection
conn.close()
# %%
