# Tweets - Republican or Democratic?

### A bare-bones Streamlit app that determines whether a tweet leans Republican or Democratic.

Built in 🐍 

using 🤗 [Transformers](https://huggingface.co/) and 

deployed [here](https://share.streamlit.io/m-newhauser/rep-or-dem-tweets/main/app.py) on Streamlit.

*Medium article coming soon.*

## Sample
All 2021 tweets (~100,000) made by all 100 United States Senators and scraped by me.

## Model

[DistilBERT base model (uncased)](https://huggingface.co/distilbert-base-uncased) for sequence classification.

## Evaluation

The model was evaluated on a validation dataset of XXXXX unseen random tweets:
```python
{'eval_accuracy': 0.878,
 'eval_f1': 0.884,
 'eval_loss': 0.31,
 'eval_precision': 0.869,
 'eval_recall': 0.899}
```
Accuracy by political party:
|            | Accuracy |
|------------|----------|
| Democrat   | xx       |
| Republican | xx       |
