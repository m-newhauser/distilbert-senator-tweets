#%%
import pandas as pd
import tweepy as tw
import numpy as np
from os import environ as env
import streamlit as st
from transformers import pipeline
import time
import psutil
import logging


@st.cache(
    allow_output_mutation=True,
    suppress_st_warning=True,
    max_entries=1,
    show_spinner=False,
)
def load_model():
    return pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-6")


def prettify_results(results):
    return max(
        list(zip(results["labels"], results["scores"])), key=lambda item: item[1]
    )


tweet_text = """
The Bipartisan Infrastructure package delivers a 
once-in-a-century investment to rebuild our nation in a stronger, 
more sustainable way. Thanks to the leadership of @POTUS and work 
of @HouseDemocrats, more jobs, safer roads, cleaner water and more
are on the way!"
"""


#%%
def main():

    st.title("Tweets - Republican or Democrat?")
    st.subheader("Which way does a tweet lean?")

    tweet_text = st.text_area(
        "Paste a tweet below:",
        "The Bipartisan Infrastructure package delivers a once-in-a-century investment to rebuild our nation in a stronger, more sustainable way. Thanks to the leadership of @POTUS and work of @HouseDemocrats, more jobs, safer roads, cleaner water and more are on the way!",
    )

    np.random.seed(123)
    labels = ["Republican", "Democrat"]
    classifier = load_model()

    if st.button("Get prediction"):

        raw_results = classifier(tweet_text, labels)
        pretty_results = prettify_results(raw_results)

        st.text("Result: {}!".format(pretty_results[0]))
        st.text("Probability score: {:.1%}".format(pretty_results[1]))


if __name__ == "__main__":
    import transformers

    transformers.logging.set_verbosity_debug()
    logging.info(f"RAM memory % used: {psutil.virtual_memory()[2]}")

    main()
