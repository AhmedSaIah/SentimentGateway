# import time
# import random
# import pickle
# import os
# from flask import Flask, jsonify, request
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.action_chains import ActionChains
# from webdriver_manager.chrome import ChromeDriverManager
# from bs4 import BeautifulSoup

# from SentimentAnalysisModel import infer
# from ApiUtils import filter_english_reviews, match_keyword

# app = Flask(__name__)

# # List of user agents to randomize
# USER_AGENTS = [
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#     'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
#     'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
#     'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
# ]

# def get_random_user_agent():
#     return random.choice(USER_AGENTS)

# def save_cookies(driver, path):
#     with open(path, 'wb') as filehandler:
#         pickle.dump(driver.get_cookies(), filehandler)

# def load_cookies(driver, path):
#     if os.path.exists(path):
#         with open(path, 'rb') as cookiesfile:
#             cookies = pickle.load(cookiesfile)
#             for cookie in cookies:
#                 driver.add_cookie(cookie)

# @app.route('/', methods=['GET', 'POST'])
# def entrance():
#     return jsonify('flask api entrance')

# @app.route('/scrapeamazon', methods=['POST'])
# def scrape_amazon():
#     try:
#         data = request.get_json()
#         assert 'url' in data, "Request must have URL in its body"
#         url = data['url']
#         keyword = data.get('keyword')

#         # Set up Chrome options
#         options = Options()
#         # Use headless mode only if necessary
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--disable-gpu')
#         options.add_argument(f'user-agent={get_random_user_agent()}')
#         options.add_argument("--window-size=1920,1080")

#         # Initialize Chrome WebDriver
#         service = Service(ChromeDriverManager().install())
#         driver = webdriver.Chrome(service=service, options=options)

#         # Load cookies if available
#         cookies_path = 'amazon_cookies.pkl'
#         load_cookies(driver, cookies_path)

#         driver.get(url)
#         time.sleep(random.uniform(5, 10))  # Random sleep to mimic human behavior

#         # Save cookies
#         save_cookies(driver, cookies_path)

#         # Perform mouse movements to mimic user
#         actions = ActionChains(driver)
#         actions.move_by_offset(random.randint(100, 500), random.randint(100, 500)).perform()
#         time.sleep(random.uniform(1, 3))
#         actions.move_by_offset(random.randint(100, 500), random.randint(100, 500)).perform()

#         # Scroll to load dynamic content
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         time.sleep(random.uniform(2, 5))

#         page_source = driver.page_source
#         soup = BeautifulSoup(page_source, 'html.parser')

#         reviews = []
#         review_elements = soup.find_all('span', {'data-hook': 'review-body'})

#         for element in review_elements:
#             review_text = element.get_text(strip=True)
#             reviews.append(review_text)

#         driver.quit()

#         english_reviews = filter_english_reviews(reviews)
#         if keyword:
#             english_reviews = match_keyword(english_reviews, keyword=keyword)

#         model_outs = infer(english_reviews)
#         outs = [[review, model_out] for review, model_out in zip(english_reviews, model_outs)]

#         return jsonify({'reviews': outs})

#     except Exception as e:
#         return jsonify({'error': str(e)})

# @app.route('/classify', methods=['POST'])
# def classify():
#     data = request.json
#     text = data['review']
#     prediction = infer(text)
#     return jsonify({'prediction': prediction})

# if __name__ == '__main__':
#     app.run(debug=True)


import os
import pickle
import random
import time

from ApiUtils import filter_english_reviews, match_keyword
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
# Replace these imports with your actual implementations
from SentimentAnalysisModel import infer
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)

# List of user agents to randomize
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
]


def get_random_user_agent():
    return random.choice(USER_AGENTS)


def save_cookies(driver, path):
    with open(path, 'wb') as filehandler:
        pickle.dump(driver.get_cookies(), filehandler)


def load_cookies(driver, path):
    if os.path.exists(path):
        with open(path, 'rb') as cookiesfile:
            cookies = pickle.load(cookiesfile)
            for cookie in cookies:
                if 'expiry' in cookie:
                    # Remove 'expiry' key to avoid exceptions
                    del cookie['expiry']
                driver.add_cookie(cookie)


def perform_human_actions(driver):
    """Perform actions to mimic human interaction."""
    actions = ActionChains(driver)
    # Move mouse
    actions.move_by_offset(random.randint(100, 200),
                           random.randint(100, 200)).perform()
    time.sleep(random.uniform(1, 3))
    actions.move_by_offset(random.randint(100, 200),
                           random.randint(100, 200)).perform()
    # Click a random part of the screen (ensure it's not an element that disrupts the process)
    actions.click().perform()


@app.route('/', methods=['GET', 'POST'])
def entrance():
    return jsonify('flask api entrance')


@app.route('/scrapeamazon', methods=['POST'])
def scrape_amazon():

    data = request.get_json()
    assert 'url' in data, "Request must have URL in its body"
    url = data['url']
    keyword = data.get('keyword')

    # Set up Chrome options
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument(f'user-agent={get_random_user_agent()}')
    options.add_argument("--window-size=1920,1080")

    # Initialize Chrome WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # Load cookies if available
    cookies_path = 'amazon_cookies.pkl'
    driver.get(url)  # Navigate to the URL before loading cookies
    load_cookies(driver, cookies_path)
    driver.refresh()  # Refresh the page to use loaded cookies

    # Perform human-like actions
    perform_human_actions(driver)

    # Random sleep to mimic human behavior
    time.sleep(random.uniform(5, 10))

    # Scroll to load dynamic content
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(random.uniform(2, 5))

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    reviews = []
    review_elements = soup.find_all('span', {'data-hook': 'review-body'})

    for element in review_elements:
        review_text = element.get_text(strip=True)
        reviews.append(review_text)

    driver.quit()

    english_reviews = filter_english_reviews(reviews)
    if keyword:
        english_reviews = match_keyword(english_reviews, keyword=keyword)

    model_outs = infer(english_reviews)

    outs = [[review] + model_out
            for review, model_out in zip(english_reviews, model_outs)]

    return jsonify({'reviews': outs})

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    text = data['review']
    prediction = infer(text)
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True)
