# Fine-tuning DistilBERT on senator tweets

### A guide to fine-tuning DistilBERT on the tweets of American Senators with snscrape, SQLite, and Transformers (PyTorch) on Google Colab.

Built in 🐍 

using 🤗 [Transformers](https://huggingface.co/) and 

deployed on Streamlit 🎈 (coming soon!).

Read the Medium article [here](https://medium.com/@mary.newhauser/fine-tuning-distilbert-on-senator-tweets-a6f2425ca50e).

## Code
Part 1: Creating the dataset - [get_tweets.ipynb](https://github.com/m-newhauser/distilbert-senator-tweets/blob/main/notebooks/get_tweets.ipynb)

Part 2: Fine-tuning DistilBERT - [finetune_distilbert_senator_tweets_pt.ipynb](https://github.com/m-newhauser/distilbert-senator-tweets/blob/main/notebooks/finetune_distilbert_senator_tweets_pt.ipynb)

## Sample
All 2021 tweets (~100,000) posted by 100 United States Senators and scraped by me.

## Model

[DistilBERT base model (uncased)](https://huggingface.co/distilbert-base-uncased) for sequence classification.

## Evaluation

The model was evaluated on a test dataset (20%):
```python
{'accuracy': 0.908, 
'f1': 0.912}
```
