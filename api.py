import os
import pickle
import random
import time
import re

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
    max_reviews = data.get('max_reviews', 20)  # Default max reviews to 100 if not provided

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

    reviews, locations = [], []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(reviews) < max_reviews:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 5))

        # Get page source and parse
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Extract review elements
        review_elements = soup.find_all('span', {'data-hook': 'review-body'})
        date_location_elements = soup.find_all('span', {'data-hook': 'review-date'})

        for review_element, location_element in zip(review_elements, date_location_elements):
            review_text = review_element.get_text(strip=True)
            location_text = extract_location(location_element.get_text(strip=True))
            
            reviews.append(review_text)
            locations.append(location_text)

            if len(reviews) >= max_reviews:
                break

        # Check if no more reviews are loaded (page did not scroll)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()

    english_reviews, english_reviews_indecies = filter_english_reviews(reviews)
    selected_locations = [locations[i] for i in english_reviews_indecies if i < len(locations)]
    matched_selected_locations = selected_locations
    
    if keyword:
        english_reviews, matched_reviews_indecies = match_keyword(english_reviews, keyword=keyword)
        matched_selected_locations = [selected_locations[i] for i in matched_reviews_indecies]
    model_outs = infer(english_reviews)
    print(matched_selected_locations)

    outs = [[review, location] + model_out
            for review, location, model_out in zip(english_reviews, matched_selected_locations, model_outs)]

    return jsonify({'reviews': outs})

def extract_location(date_location_text):
    """
    Extracts the location from the review date-location text.
    Assumes format 'Reviewed in <Location> on <Date>'.
    """
    match = re.search(r'Reviewed in (.*?) on ', date_location_text)
    if match:
        return match.group(1)
    return "Unknown"

@app.route('/classify', methods=['POST'])
def classify():
    data = request.json
    text = data['review']
    prediction = infer(text)
    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True)
