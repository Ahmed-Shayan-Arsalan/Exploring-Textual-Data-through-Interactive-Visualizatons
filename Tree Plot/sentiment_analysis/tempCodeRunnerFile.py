from flask import Flask, render_template, request
import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

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

    sentiment_words = analyze_sentiment_words(text)

    graph_data = {
        "nodes": [
            {"id": sentiment, "top_words": sentiment_words[sentiment][:10]} for sentiment in sentiment_words
        ],
        "links": [
            {"source": sentiment, "target": word["word"]} for sentiment in sentiment_words for word in sentiment_words[sentiment][:10]
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

    sentiment_words = {
        "Angry": [],
        "Anticipation": [],
        "Fear": [],
        "Sad": [],
        "Happy": []
    }

    for word, score in word_sentiment:
        if score < -0.5:
            sentiment_words["Angry"].append({"word": word, "intensity": score})
        elif 0.1 < score < 0.5:
            sentiment_words["Anticipation"].append({"word": word, "intensity": score})
        elif score < -0.2:
            sentiment_words["Fear"].append({"word": word, "intensity": score})
        elif score < 0:
            sentiment_words["Sad"].append({"word": word, "intensity": score})
        elif score > 0:
            sentiment_words["Happy"].append({"word": word, "intensity": score})

    # Sort words within each sentiment category based on intensity
    for sentiment in sentiment_words:
        sentiment_words[sentiment].sort(key=lambda x: x["intensity"])

    return sentiment_words

if __name__ == '__main__':
    app.run(debug=True)
