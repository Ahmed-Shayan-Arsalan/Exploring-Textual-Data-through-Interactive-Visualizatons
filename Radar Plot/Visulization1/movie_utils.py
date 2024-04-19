import json
import random

def get_unique_movies(file_path_speakers):
    with open(file_path_speakers, 'r') as file:
        data_speakers = json.load(file)

    unique_movies = list(set(value['meta']['movie_name'] for value in data_speakers.values()))
    return unique_movies

def get_top_characters_for_movie(file_path_speakers, movie_name, num_characters=3):
    with open(file_path_speakers, 'r') as file:
        data_speakers = json.load(file)

    characters_for_movie = [value for value in data_speakers.values() if value['meta']['movie_name'] == movie_name]
    characters_sorted = sorted(characters_for_movie, key=lambda x: int(x['meta']['credit_pos']) if x['meta']['credit_pos'].isdigit() else float('inf'))
    top_characters = characters_sorted[:num_characters]

    return top_characters

def get_random_movies(file_path_speakers, num_movies=5):
    unique_movies = get_unique_movies(file_path_speakers)
    selected_movies = random.sample(unique_movies, num_movies)
    return selected_movies
