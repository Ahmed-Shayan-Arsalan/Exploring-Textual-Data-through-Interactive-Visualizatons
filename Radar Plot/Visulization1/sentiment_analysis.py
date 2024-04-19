import json
from textblob import TextBlob
from nrclex import NRCLex

def analyze_character(file_path_utterances, character_name, character_id, min_text_length=10, num_conversations=10):
    with open(file_path_utterances, 'r') as file:
        utterances = [json.loads(line) for line in file]

    conversations = []
    for utterance in utterances:
        if utterance['speaker'] == character_id:
            conversation_id = utterance['conversation_id']
            text = utterance['text']

            # Check if the conversation text is long enough
            if len(text.split()) >= min_text_length:
                conversations.append((conversation_id, text))

    # Analyze sentiment and emotion for each long enough utterance in the conversations
    sentiment_scores = []
    emotion_scores_list = []
    for _, text in conversations:
        blob = TextBlob(text)
        sentiment_scores.append(blob.sentiment.polarity)

        emotion_scores = NRCLex(text).affect_frequencies
        emotion_scores_list.append(emotion_scores)

    # Ensure that all emotions are present in each dictionary
    for emotion in emotion_scores_list[0].keys():
        for scores in emotion_scores_list:
            if emotion not in scores:
                scores[emotion] = 0.0

    # Calculate the average emotion scores
    avg_emotion_scores = {emotion: sum(scores[emotion] for scores in emotion_scores_list) / len(emotion_scores_list)
                          for emotion in emotion_scores_list[0]}

    # Calculate the average sentiment score
    avg_sentiment_score = sum(sentiment_scores) / len(sentiment_scores)

    # Return the results as a dictionary
    result_dict = {
        "Character ID": character_id,
        "Character Name": character_name,
        "Final Scores": {
            "Average Sentiment Score": avg_sentiment_score,
            "Average Emotion Scores": avg_emotion_scores
        }
    }

    return result_dict

def analyze_sentiment_for_top_characters(utterances_file_path, data_speakers_path, selected_movie, selected_characters):
    with open(data_speakers_path, 'r') as file:
        data_speakers = json.load(file)

    # Get character IDs for the selected characters in the selected movie
    character_ids = []
    for character_name in selected_characters:
        character_id = next(key for key, value in data_speakers.items()
                           if value['meta']['character_name'] == character_name
                           and value['meta']['movie_name'] == selected_movie)
        character_ids.append(character_id)

    # List to store results for each character
    all_results = []

    for character_name, character_id in zip(selected_characters, character_ids):
        # Analyze the character and store the results in the list
        results = analyze_character(utterances_file_path, character_name, character_id, min_text_length=10, num_conversations=50)
        all_results.append(results)

    return all_results
