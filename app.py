# app.py

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
    return pipeline("zero-shot-classification")


def prettify_results(results):
    return max(
        list(zip(results["labels"], results["scores"])), key=lambda item: item[1]
    )


def main():

    st.title("Tweets - Republican or Democrat?")
    st.subheader("Which way does a tweet lean?")

    tweet_text = st.text_area(
        "Paste a tweet below:",
        "Major NY14 climate victory today! Earlier this year, fossil fuel co NRG began to rush high-pollution, fracked-gas peaker plants into our community. We organized all year against it while securing wind + solar projects. Today the plant was denied. When we mobilize, we win",
    )

    if st.button("Get prediction"):
        # my_bar = st.progress(0)

        # for percent_complete in range(100):
        #     time.sleep(0.1)
        #     my_bar.progress(percent_complete + 1)
        np.random.seed(123)
        classifier = load_model()
        labels = ["Republican", "Democrat"]
        raw_results = classifier(tweet_text, labels)
        pretty_results = prettify_results(raw_results)

        st.text("Result: {}!".format(pretty_results[0]))
        st.text("Probability score: {:.1%}".format(pretty_results[1]))


if __name__ == "__main__":
    import os

    logging.info(f"RAM memory % used: {psutil.virtual_memory()[2]}")

    main()
