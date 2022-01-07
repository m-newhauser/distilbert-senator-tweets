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
START_DATE = "2021-01-20"  # YYYY-MM-DD
END_DATE = "2021-12-31"  # YYYY-MM-DD

# %%
# Convert date strings for later pd.query()
START_DATE = START_DATE.replace("-", "")
END_DATE = END_DATE.replace("-", "")

# %%
# Get all tweets for given username
scraped_profile = twitter.TwitterProfileScraper(username="SenSanders").get_items()

# Extract only necessary data
tweets = [
    {
        "date": tweet.date.strftime(DATETIME_FORMAT),
        "id": tweet.id,
        "username": tweet.user.username,
        "text": tweet.content,
        "is_retweet": str(tweet.retweetedTweet),
    }
    for tweet in scraped_profile
]

# %%
# Put tweet data into a df
tweets_df = pd.DataFrame(tweets)

# Tidy up
tweets_df = (
    tweets_df.query('is_retweet == "None"')  # remove all retweets
    .assign(date=pd.to_datetime(tweets_df.date))  # convert col from str to datetime
    .query(f"{START_DATE} < date < {END_DATE}")  # drop tweets outside of date range
    .drop(columns=["is_retweet"])  # drop col
    .sort_values(by=["date"])  # sort by date
    .reset_index(drop=True)
)

# %%
# Connect to locally created db (and create if it doesn't exist)
conn = sqlite3.connect("data/TWEETS.db")  # Command palette > SQLite: Open database

# Write df to (new) table in db
tweets_df.to_sql("senators", conn, if_exists="append", chunksize=10000)

# # Run a test query
# df = pd.read_sql_query("SELECT * from senators LIMIT 10", conn)

# %%
# Close connection
conn.close()
