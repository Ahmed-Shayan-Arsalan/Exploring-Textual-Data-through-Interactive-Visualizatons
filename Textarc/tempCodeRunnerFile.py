from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import numpy as np
import re
import nltk
from nltk import sent_tokenize, word_tokenize, pos_tag, ne_chunk

app = Flask(__name__)

nltk.download('punkt')
nltk.download('maxent_ne_chunker')
nltk.download('words')

def process_text(text):
    # Split the text into sentences using NLTK's sentence tokenizer
    sentences = sent_tokenize(text)

    # Perform Named Entity Recognition (NER) on each sentence
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

def plot_sentences_around_circle(text, search_word=None):
    ner_sentences = process_text(text)

    # Create a circle of points
    num_sentences = len(ner_sentences)
    theta = np.linspace(0, 2 * np.pi, num_sentences, endpoint=False)

    # Set up the plot with a larger figure size
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(10, 10))
    ax.set_theta_offset(np.pi/2)  # Set the starting point at the top

    # Display each NER sentence around the circle with individual space
    for i, ner_sentence in enumerate(ner_sentences):
        ner_sentence = ner_sentence.strip()  # Remove leading and trailing whitespaces

        # Calculate the adjusted angle for each line
        adjusted_theta = i * (2 * np.pi / num_sentences)

        # Draw lines from the center to the outer edge of the circle
        line_theta = i * (2 * np.pi / num_sentences)

        if search_word and search_word.lower() in ner_sentences[i].lower():
            ax.plot([0, line_theta], [0, 1], color='red', linestyle='dashed')
        else:
            ax.plot([0, line_theta], [0, 1], color='black', linestyle='dashed')

        ax.text(adjusted_theta, 1, ner_sentence, ha='center', va='center', wrap=True, rotation=adjusted_theta*180/np.pi)

    # Remove the polar grid lines for a cleaner look
    ax.set_yticklabels([])
    ax.set_xticklabels([])

    plt.savefig('static/circle_plot.png')  # Save the plot as an image


@app.route('/', methods=['GET', 'POST'])
def index():
    search_word = None
    if request.method == 'POST':
        search_word = request.form.get('search_word')

    with open('Alice.txt', 'r', encoding='utf-8') as file:
        text = file.read()

    plot_sentences_around_circle(text, search_word)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
