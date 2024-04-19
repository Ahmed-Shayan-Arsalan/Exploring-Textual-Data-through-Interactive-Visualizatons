from flask import Flask, render_template, request, jsonify
from sentiment_analysis import analyze_sentiment_for_top_characters
from movie_utils import get_unique_movies, get_top_characters_for_movie
from visualization import save_combined_radar_chart  # Import the visualization function

app = Flask(__name__)

@app.route('/')
def index():
    file_path_speakers = 'D:\\Downloads\\Mcorpus\\movie-corpus\\speakers.json'
    movies = get_unique_movies(file_path_speakers)
    return render_template('index.html', movies=movies)

@app.route('/get_top_characters', methods=['POST'])
def get_top_characters():
    file_path_speakers = 'D:\\Downloads\\Mcorpus\\movie-corpus\\speakers.json'
    selected_movie = request.form.get('selected_movie')
    top_characters = get_top_characters_for_movie(file_path_speakers, selected_movie, num_characters=3)
    return render_template('top_characters.html', characters=top_characters, movie=selected_movie)

@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    utterances_file_path = 'D:\\Downloads\\Mcorpus\\movie-corpus\\utterances.jsonl'
    data_speakers_path = 'D:\\Downloads\\Mcorpus\\movie-corpus\\speakers.json'

    selected_movie = request.form.get('selected_movie')
    selected_characters = request.form.getlist('selected_characters[]')

    # Analyze sentiment for the selected characters in the selected movie
    results = analyze_sentiment_for_top_characters(utterances_file_path, data_speakers_path, selected_movie, selected_characters)

    # Pass the sentiment results to the visualization function
    save_combined_radar_chart(results)

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
