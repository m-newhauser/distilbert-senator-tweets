#%%
import pandas as pd
import numpy as np
import csv
from pandas.core.reshape.pivot import crosstab
import preprocessor as p
from transformers import pipelines
from app import load_model, prettify_results

#%%

# Load data from fivethirtyeight
senator_tweets = pd.read_csv("data/senators.csv")

# Remove numbers, emojis and &'s
p.set_options(p.OPT.NUMBER, p.OPT.EMOJI)
senator_tweets["text_clean"] = senator_tweets["text"].apply(p.clean)
senator_tweets["text_clean"] = senator_tweets["text_clean"].str.replace("&amp;", "and ")

#%%
# Load classifier
classifier = load_model()

#%%
# Get predictions
labels = ["Republican", "Democrat"]
texts = senator_tweets["text_clean"]
outputs = classifier(texts, labels)

#%%
# Clean predictions
labels = []
scores = []
for output in outputs:
    labels.append(
        [
            label
            for label, score in zip(output["labels"], output["scores"])
            if score > 0.5
        ][0]
    )
    scores.append([score for score in output["scores"] if score > 0.5][0])
final_outputs = list(zip(labels, scores))

# Append predictions to data frame
final_output_df = pd.DataFrame(final_outputs, columns=["pred", "score"])
senator_tweets["pred"] = final_output_df["pred"]
senator_tweets["score"] = final_output_df["score"]

# Move this later
senator_tweets["party"] = np.where(
    senator_tweets["party"] == "R", "Republican", "Democrat"
)

#%%
# Calculate prediction accuracy
senator_tweets["accurate"] = np.where(
    senator_tweets["party"] == senator_tweets["pred"], 1, 0
)
# %%
pd.crosstab(senator_tweets["party"], senator_tweets["pred"])

# %%
# # Write results to csv
# senator_tweets.to_csv("data/senators_results.csv", index=False)
# %%
