from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Define the API endpoint
API_URL = 'http://127.0.0.1:5000/sentimentanalysis'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['text']
    payload = {'text': text}
    headers = {'Content-Type': 'application/json'}
    
    # Make the POST request to the sentiment analysis API
    response = requests.post(API_URL, headers=headers, data=json.dumps(payload))
    
    if response.status_code == 200:
        result = response.json()
        return jsonify({'sentiment_score': result['sentiment_score']})
    else:
        return jsonify({'error': response.text})

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Running on a different port to avoid conflict
