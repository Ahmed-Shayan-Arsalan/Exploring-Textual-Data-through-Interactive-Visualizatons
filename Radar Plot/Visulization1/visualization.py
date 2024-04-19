import json
import plotly.graph_objects as go
import plotly.offline as pyo

def save_combined_radar_chart(sentiment_results):
    # Create a radar chart
    fig = go.Figure()

    # Extract emotion scores for all characters
    all_emotion_scores = [result["Final Scores"]["Average Emotion Scores"] for result in sentiment_results]

    # Get the maximum emotion score across all characters
    max_emotion_score = max(max(scores.values()) for scores in all_emotion_scores)

    # Loop through each character's data
    for result in sentiment_results:
        character_name = result["Character Name"]
        emotion_scores = result["Final Scores"]["Average Emotion Scores"]

        fig.add_trace(go.Scatterpolar(
            r=list(emotion_scores.values()) + [list(emotion_scores.values())[0]],
            theta=list(emotion_scores.keys()) + [list(emotion_scores.keys())[0]],
            fill='toself',
            name=f'{character_name} - Emotion Scores',
        ))

    # Set layout for the radar chart
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max_emotion_score],  # Adjust the range dynamically based on the maximum emotion score
            ),
        ),
        showlegend=True,
        title='Combined Radar Chart of Emotion Scores',
    )

    # Save the interactive chart as an HTML file
    pyo.plot(fig, filename='combined_emotion_radar_chart.html', auto_open=True)

# If you want to run this script independently (not from Flask), uncomment the code below
# json_file_path = 'rear_window_sent.json'
# with open(json_file_path, 'r') as json_file:
#     sentiment_results = json.load(json_file)
# save_combined_radar_chart(sentiment_results)
