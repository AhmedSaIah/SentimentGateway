import json

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st


def classify_reviews(product_url, keyword=None, max_reviews=20):
    """
    Classifies reviews for a given Amazon product URL.

    Args:
        product_url (str): The Amazon product URL.
        keyword (str, optional): A keyword to filter reviews. Defaults to None.
        max_reviews (int, optional): Maximum number of reviews to scrape. Defaults to 20.

    Returns:
        list: A list of classified reviews, or an error message.
    """
    url = 'http://127.0.0.1:5000/scrapeamazon'
    try:
        # Prepare the payload
        payload = {'url': product_url, 'max_reviews': max_reviews}
        if keyword:
            payload['keyword'] = keyword
        
        headers = {'Content-Type': 'application/json'}
        
        # Send the POST request to the scraping endpoint
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            return result['reviews']
        else:
            return f'Error: {response.status_code}, {response.text}'
    except Exception as e:
        return f'Exception: {str(e)}'

def classify_single_review(product_url):
    url = 'http://127.0.0.1:5000/classify'
    try:
        payload = {'review': product_url}
        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        
        if response.status_code == 200:
            result = response.json()
            return result['prediction'][0]
        else:
            return f'Error: {response.status_code}, {response.text}'
    except Exception as e:
        return f'Exception: {str(e)}'

# Streamlit UI
st.title("Amazon Review Classifier")

# Input text field for the Amazon link
amazon_link = st.text_input("Enter Amazon Product Link")

# optional keyword input
keyword = st.text_input("Enter Keyword (Optional)")

# Initialize session state for classification results
if 'results' not in st.session_state:
    st.session_state['results'] = None


# Button to trigger classification for Amazon link
if st.button("Classify Reviews"):
    if amazon_link:
        # Call the classify_reviews function with the input URL and keyword
        st.session_state['results'] = classify_reviews(amazon_link, keyword)
    
        if st.session_state['results']:
        # Convert results to a DataFrame for display
            df = pd.DataFrame(st.session_state['results'], columns=["Review", "Class", "Negative Probability", "Positive Probability"])
            
            # Display the results in a table
            st.write("Classification Results")
            st.table(df)   
            positive_count = sum(1 for review in st.session_state['results'] if review[-1] > review[-2])
            negative_count = len(st.session_state['results']) - positive_count
            # print(negative_count,positive_count)
            # Plot pie chart
            labels = 'Positive', 'Negative'
            sizes = [positive_count, negative_count]
            colors = ['lightgreen', 'lightcoral']
            explode = (0.1, 0)  # explode the 1st slice (Positive)

            fig, ax = plt.subplots()
            ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
            ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

            st.write("Pie Chart of Review Sentiments")
            st.pyplot(fig)
        else:
            st.write("No reviews was found with the keyword provided")
    else:
        st.error("Please enter a valid Amazon product link.")
            
# Input text area for a single review
single_review = st.text_area("Enter a Single Review")

# Button to classify the single review
if st.button("Classify Single Review"):
    if single_review:
        # Call the classify_single_review function with the input review
        probabilities = classify_single_review(single_review)
        
        # Prepare the result for display
        single_review_result = {"Review": [single_review],
                                "Class": [probabilities[0]],
                                "Negative Probability": [probabilities[1]],
                                "Positive Probability": [probabilities[2]]}
        
        # Convert the result to a DataFrame for display
        df_single = pd.DataFrame(single_review_result)
        
        # Display the result in a table
        st.write("Single Review Classification")
        st.table(df_single)
    else:
        st.error("Please enter a review to classify.")