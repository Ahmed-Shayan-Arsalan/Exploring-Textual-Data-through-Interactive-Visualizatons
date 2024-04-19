from flask import Flask, render_template, request
import numpy as np
import re
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk
import json

app = Flask(__name__)

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def process_text(text):
    sentences = sent_tokenize(text)
    ner_sentences = []

    for sentence in sentences:
        words = word_tokenize(sentence)
        pos_tags = pos_tag(words)
        ner_tree = ne_chunk(pos_tags)
        ner_sentences.append(' '.join([word if type(word) is str else word[0] for word in ner_tree.flatten()]))

    return ner_sentences

def polar2cart(r, theta):
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def generate_circle_data(text, search_word=None):
    ner_sentences = process_text(text)
    num_sentences = len(ner_sentences)
    theta = np.linspace(0, 2 * np.pi, num_sentences, endpoint=False)

    circle_data = []
    for i, ner_sentence in enumerate(ner_sentences):
        ner_sentence = ner_sentence.strip()
        adjusted_theta = i * (2 * np.pi / num_sentences)
        x, y = polar2cart(250, adjusted_theta)
        angle = adjusted_theta - (np.pi / 2)

        # Check if the search word is present in the sentence
        highlight = search_word and search_word.lower() in ner_sentence.lower()

        circle_data.append({
            "x": x + 300,
            "y": y + 300,
            "text": ner_sentence,
            "angle": angle,
            "highlight": highlight,
        })

    return circle_data

def save_circle_data_as_json(text, search_word=None):
    circle_data = generate_circle_data(text, search_word)
    with open('static/circle_plot.json', 'w') as json_file:
        json.dump(circle_data, json_file)

@app.route('/', methods=['GET', 'POST'])
def index():
    search_word = None
    if request.method == 'POST':
        search_word = request.form.get('search_word')

    with open('Alice.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    save_circle_data_as_json(text, search_word)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
