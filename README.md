# Sentiment Analysis API

This project provides an API for classifying Amazon product reviews into positive and negative sentiments using a DistilBERT-based classifier. It includes functionalities to scrape reviews from Amazon and a Streamlit UI for user interaction.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Setup](#setup)
- [Running the API](#running-the-api)
- [Running the Streamlit UI](#running-the-streamlit-ui)
- [Usage](#usage)
- [Project Structure](#project-structure)

## Overview

The API allows users to:
1. Scrape reviews from Amazon product pages.
2. Classify the reviews into positive or negative sentiments.
3. Visualize the distribution of sentiments using a pie chart.

## Features

- Scrape Amazon reviews from a provided URL.
- Classify reviews using a DistilBERT-based model.
- Display results and visualizations in a Streamlit UI.

## Setup

### Prerequisites

- Python 3.12
- `pip` 

### Dependencies

Install the required dependencies using `pip`:

```bash
pip install -r requirements.txt
```

## Running the api
```bash```
```cd ~ ``` 
```workon sentiment```
```bash run_sentiment_server.sh ```

## Running the ui
```bash```
```cd ~```
```workon sentiment```
```bash run_sentiment_ui.sh ```

# Ensure that your requirements.txt includes:

streamlit
flask
beautifulsoup4
requests
transformers
torch
pandas
matplotlib
webdriver-manager
selenium

## Project Structure

Sentiment/
│
SentimentGateway/
│
├── ApiUtils.py                      
├── api.py    
├── client.py
├── UI.py
├── requirements.txt                 # Project dependencies
├── SentimentAnalysis/           # Model inference functions
    └── ModelsRepository/
        └── model.pt
    └── Utils/
    └── __init__.py
    └── Inference.py
    └── main.py
