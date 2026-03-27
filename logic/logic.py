import random
from collections import Counter


# ─────────────────────────────────────────────
#  KEYWORD DICTIONARIES
# ─────────────────────────────────────────────

POSITIVE_KEYWORDS = {
    "good", "great", "excellent", "clean", "improved", "fixed",
    "resolved", "happy", "satisfied", "working", "better", "fast",
    "efficient", "smooth", "reliable", "safe", "clear", "available",
}

NEGATIVE_KEYWORDS = {
    "bad", "poor", "dirty", "broken", "issue", "problem", "complaint",
    "failure", "slow", "blocked", "leak", "damaged", "unsafe", "outage",
    "shortage", "contaminated", "flooded", "missing", "stuck", "dead",
}

TOPIC_KEYWORDS = {
    "water":       {"water", "leak", "pipe", "supply", "drainage", "flood", "contaminated"},
    "electricity": {"electricity", "power", "outage", "voltage", "wire", "light", "meter"},
    "pollution":   {"pollution", "smoke", "garbage", "waste", "smell", "toxic", "dirty"},
    "traffic":     {"traffic", "road", "signal", "jam", "pothole", "blocked", "vehicle"},
}


# ─────────────────────────────────────────────
#  1. SENTIMENT ANALYSIS
# ─────────────────────────────────────────────

def analyze_sentiment(text: str) -> str:

    if not isinstance(text, str) or not text.strip():
        return "Neutral"

    tokens = set(text.lower().split())
    pos_hits = len(tokens & POSITIVE_KEYWORDS)
    neg_hits = len(tokens & NEGATIVE_KEYWORDS)

    if pos_hits > neg_hits:
        return "Positive"
    elif neg_hits > pos_hits:
        return "Negative"
    else:
        return "Neutral"


# ─────────────────────────────────────────────
#  2. SCORE MAPPING
# ─────────────────────────────────────────────

def sentiment_to_score(sentiment: str) -> int:

    ranges = {
        "Positive": (7, 10),
        "Neutral":  (4, 6),
        "Negative": (1, 3),
    }
    low, high = ranges.get(sentiment, (4, 6))
    return random.randint(low, high)


def analyze_sentiment_with_score(text: str) -> dict:

    sentiment = analyze_sentiment(text)
    score     = sentiment_to_score(sentiment)
    return {"sentiment": sentiment, "score": score}


# ─────────────────────────────────────────────
#  3. TOPIC DETECTION
# ─────────────────────────────────────────────

def detect_topics(text: str) -> list[str]:
 
    if not isinstance(text, str) or not text.strip():
        return []

    tokens  = set(text.lower().split())
    matched = [
        topic
        for topic, keywords in TOPIC_KEYWORDS.items()
        if tokens & keywords
    ]
    return matched


def detect_primary_topic(text: str) -> str | None:

    topics = detect_topics(text)
    if not topics:
        return None

    # Score each topic by keyword overlap count
    tokens = set(text.lower().split())
    scores = {
        topic: len(tokens & TOPIC_KEYWORDS[topic])
        for topic in topics
    }
    return max(scores, key=scores.get)


# ─────────────────────────────────────────────
#  4. WARD FREQUENCY ANALYSIS
# ─────────────────────────────────────────────

from collections import Counter

def compute_ward_frequency(entries: list[dict]) -> dict:
    ward_data: dict[str, dict] = {}

    for entry in entries:
        ward = entry.get("ward", "").strip()
        text = entry.get("text", "")

        if not ward:
            continue

        if ward not in ward_data:
            ward_data[ward] = {"count": 0, "topic_counts": Counter()}

        ward_data[ward]["count"] += 1

        topic = detect_primary_topic(text)
        if topic:
            ward_data[ward]["topic_counts"][topic] += 1

    # Build final output
    result = {}
    for ward, data in ward_data.items():
        top_issue = (
            data["topic_counts"].most_common(1)[0][0]
            if data["topic_counts"]
            else "others"   
        )

        result[ward] = {
            "count": data["count"],
            "top_issue": top_issue,
        }

    return result

# ─────────────────────────────────────────────
#  5. FULL PIPELINE  (convenience wrapper)
# ─────────────────────────────────────────────

def process_entry(entry: dict) -> dict:

    text            = entry.get("text", "")
    sentiment_data  = analyze_sentiment_with_score(text)

    return {
        "ward":          entry.get("ward", ""),
        "text":          text,
        "sentiment":     sentiment_data["sentiment"],
        "score":         sentiment_data["score"],
        "topics":        detect_topics(text),
        "primary_topic": detect_primary_topic(text),
    }


# ─────────────────────────────────────────────
#  QUICK DEMO
# ─────────────────────────────────────────────

if __name__ == "__main__":
    sample_entries = [
        {"ward": "Rohini",   "text": "There is a water leak on the main road."},
        {"ward": "Rohini",   "text": "Power outage for 3 days, no electricity."},
        {"ward": "Rohini",   "text": "Water supply is clean and working fine."},
        {"ward": "Dwarka",   "text": "Garbage dumped everywhere, terrible pollution."},
        {"ward": "Dwarka",   "text": "Traffic jam near the signal every morning."},
        {"ward": "Janakpuri","text": "Road is blocked and there is a bad smell."},
        {"ward": "Rohini",   "text": "Pipe is broken, contaminated water supply."},
        {"ward": "Janakpuri","text": "Electricity meter is damaged and dead."},
    ]

    print("=" * 55)
    print("  PER-ENTRY ANALYSIS")
    print("=" * 55)
    for entry in sample_entries:
        result = process_entry(entry)
        print(
            f"[{result['ward']:10}] {result['sentiment']:8} "
            f"| score={result['score']} "
            f"| topic={result['primary_topic']}"
        )

    print("\n" + "=" * 55)
    print("  WARD FREQUENCY SUMMARY")
    print("=" * 55)
    ward_summary = compute_ward_frequency(sample_entries)
    for ward, stats in ward_summary.items():
        print(f"  {ward:12} → count={stats['count']}, top_issue={stats['top_issue']}")