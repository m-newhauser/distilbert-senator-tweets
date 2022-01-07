## Extract senator twitter handles from a CSV
## Data source: https://ucsd.libguides.com/congress_twitter

#%%
import pandas as pd

#%%
# Read data from UTF-8 encoded CSV
df = pd.read_csv(
    "/Users/mnewhauser/python-work/rep-or-dem-tweets/data/congress_twitter_senate.csv"
)

# Extract usernames
usernames_df = (
    df.assign(username=df.Link.str.split("/").str[-1])
    .drop(columns=["Link"])
    .rename(columns=str.lower)
)

# Write to CSV
usernames_df.to_csv(
    "/Users/mnewhauser/python-work/rep-or-dem-tweets/data/senators_usernames.csv"
)
