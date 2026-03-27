import json
from collections import Counter, defaultdict
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))  # polinex/

sys.path.append(PROJECT_ROOT)

from logic.logic import process_entry, compute_ward_frequency

# Load data
def load_data():
    import os
    import json

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # backend/
    PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))  # polinex/
    DATA_PATH = os.path.join(PROJECT_ROOT, "data", "dataset.json")

    with open(DATA_PATH, "r") as f:
        return json.load(f)

# Analyze sentiments
def analyze_data(data):
    processed = [process_entry(item) for item in data]

    positive = negative = neutral = 0
    scores = []
    topics = []

    for item in processed:
        sentiment = item["sentiment"].lower()
        score = item["score"]
        topic = item["primary_topic"]

        scores.append(score)
        if topic:
            topics.append(topic)

        if sentiment == "positive":
            positive += 1
        elif sentiment == "negative":
            negative += 1
        else:
            neutral += 1

    avg_score = sum(scores) / len(scores) if scores else 0
    top_topics = [t[0] for t in Counter(topics).most_common(3)]

    return {
        "positive": positive,
        "negative": negative,
        "neutral": neutral,
        "top_topics": top_topics,
        "avg_score": round(avg_score, 2)
    }
def generate_heatmap(data):
    return compute_ward_frequency(data)

# Summary generator
def generate_summary(data):
    total = len(data)
    sentiments = analyze_data(data)

    summary = (
        f"Total reports: {total}. "
        f"Positive: {sentiments['positive']}, "
        f"Negative: {sentiments['negative']}, "
        f"Neutral: {sentiments['neutral']}. "
        f"Top issues include: {', '.join(sentiments['top_topics'])}."
    )

    return summary