# from flask import Flask, request, jsonify
# from textblob import TextBlob
# import requests
# from bs4 import BeautifulSoup
# import re

# app = Flask(__name__)

# @app.route('/', methods=['GET','POST'])
# def entrance():
#     return jsonify({'flask api entrance'})

# # Endpoint for sentiment analysis
# @app.route('/sentimentanalysis', methods=['POST'])
# def sentiment_analysis():
#     try:
#         data = request.get_json()
#         text = data['text']
#         analysis = TextBlob(text)
#         sentiment_score = analysis.sentiment.polarity
#         return jsonify({'sentiment_score': sentiment_score})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# # Endpoint to scrape Amazon reviews
# @app.route('/scrapeamazon', methods=['POST'])
# def scrape_amazon():
#     try:
#         data = request.get_json()
#         url = data['url']
        
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
#         }
        
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.content, 'html.parser')
        
#         reviews = []
        
#         # Amazon review selector - might need to adjust based on the actual structure
#         review_elements = soup.find_all('span', {'data-hook': 'review-body'})
        
#         for element in review_elements:
#             review_text = element.get_text(strip=False)
#             reviews.append(review_text)
        
#         return jsonify({'reviews': reviews})
#     except Exception as e:
#         return jsonify({'error': str(e)})

# if __name__ == '__main__':
#     app.run(debug=True)

# # @app.route('/sentimentanalysis', methods=['POST'])
# # def sentiment_analysis():
# #     try:
# #         # Extract the raw text from the request
# #         data = request.get_json()
# #         text = data['text']
        
# #         # Perform sentiment analysis using TextBlob
# #         analysis = TextBlob(text)
# #         sentiment_score = analysis.sentiment.polarity
        
# #         # Return the sentiment score
# #         return jsonify({'sentiment_score': sentiment_score})
# #     except Exception as e:
# #         return jsonify({'error': str(e)})

# # if __name__ == '__main__':
# #     app.run(debug=True)

from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException
import time

DetectorFactory.seed = 0

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def entrance():
    return jsonify('flask api entrance')

def filter_english_reviews(reviews):
    english_reviews = []
    for review in reviews:
        try:
            if detect(review) == 'en':
                english_reviews.append(review)
        except LangDetectException:
            continue
    return english_reviews

@app.route('/scrapeamazon', methods=['POST'])
def scrape_amazon():
    try:
        data = request.get_json()
        url = data['url']

        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        time.sleep(5)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        
        reviews = []
        review_elements = soup.find_all('span', {'data-hook': 'review-body'})
        
        for element in review_elements:
            review_text = element.get_text(strip=True)
            reviews.append(review_text)
        
        driver.quit()
        
        english_reviews = filter_english_reviews(reviews)
        return jsonify({'reviews': english_reviews})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
