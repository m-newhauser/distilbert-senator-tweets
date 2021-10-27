# Get party information and Twitter UIDs for politicians
# Both CSVs were downloaded from http://twitterpoliticians.org/download
# %%
import pandas as pd

# %%
# Import data
members_raw = pd.read_csv(
    "data/full_member_info.csv", encoding="utf16", engine="python"
)

# %%
# Clean data
# Keep only relevant columns
members = members_raw[
    [
        "country",
        "name",
        "party",
        "uid",
        "legislative_start_date",
        "legislative_end_date",
    ]
].copy()

# Fill NAs with 0 so we can convert from float to int
members = members.fillna(0)

# Convert to int
members["uid"] = members["uid"].astype(int)
