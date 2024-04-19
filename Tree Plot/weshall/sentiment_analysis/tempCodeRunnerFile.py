from flask import Flask, render_template, request
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from collections import Counter

nltk.download('punkt')
nltk.download('vader_lexicon')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    if 'file' not in request.files:
        return render_template('index.html', error='No file part')

    file = request.files['file']

    if file.filename == '':
        return render_template('index.html', error='No selected file')

    text = file.read().decode('utf-8')

    sad_words, happy_words = analyze_sentiment_words(text)

    graph_data = {
        "nodes": [
            {"id": "Sad"},
            {"id": "Happy"}
        ],
        "links": [
            {"source": "Sad", "target": word} for word in sad_words[:10]
        ] + [
            {"source": "Happy", "target": word} for word in happy_words[:10]
        ]
    }

    graph_data_json = json.dumps(graph_data)

    return render_template('index.html', graph_data=graph_data_json)

def analyze_sentiment_words(text):
    sia = SentimentIntensityAnalyzer()
    tokens = word_tokenize(text)
    sentiment_scores = [sia.polarity_scores(token)['compound'] for token in tokens]

    word_sentiment = list(zip(tokens, sentiment_scores))
    word_sentiment.sort(key=lambda x: x[1])

    sad_words = [word for word, score in word_sentiment if score < 0]
    happy_words = [word for word, score in word_sentiment if score > 0]

    return sad_words, happy_words

if __name__ == '__main__':
    app.run(debug=True)
