import json

import requests

# Define the API endpoint
url = 'http://127.0.0.1:5000/scrapeamazon'

# Function to scrape Amazon reviews
def scrape_reviews(product_url):
    try:
        payload = {'url': product_url}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            return result['reviews']
        else:
            return f'Error: {response.status_code}, {response.text}'
    except Exception as e:
        return f'Exception: {str(e)}'

if __name__ == '__main__':
    # Example Amazon product URL (ensure it includes reviews)
    product_url = input("Enter Amazon product URL: ")
    reviews = scrape_reviews(product_url)
    for i, review in enumerate(reviews):
        print(f"Review {i+1}: {review}")
