import json
from collections import Counter, defaultdict

# Load data
def load_data():
    with open("data.json", "r") as f:
        return json.load(f)

# Analyze sentiments
def analyze_data(data):
    positive = negative = neutral = 0
    scores = []
    topics = []

    for item in data:
        sentiment = item.get("sentiment", "").lower()
        score = item.get("score", 0)
        topic = item.get("topic", "")

        scores.append(score)
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

# Ward heatmap
def generate_heatmap(data):
    ward_data = defaultdict(list)

    for item in data:
        ward = item.get("ward")
        topic = item.get("topic")
        ward_data[ward].append(topic)

    result = {}
    for ward, topics in ward_data.items():
        top_issue = Counter(topics).most_common(1)[0][0]
        result[ward] = {
            "count": len(topics),
            "top_issue": top_issue
        }

    return result

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