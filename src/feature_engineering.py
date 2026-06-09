import pandas as pd

severity_keywords = {
    "outage": 5,
    "fraud": 5,
    "hacked": 5,
    "stolen": 5,
    "payment failed": 4,
    "unauthorized": 4,
    "error": 3,
    "failed": 3,
    "urgent": 2,
    "asap": 1,
    "login": 1,
    "password": 1
}

def combine_text(subject, description):
    return f"{subject} {description}"

def keyword_score(text):
    text = str(text).lower()
    score = 0

    for word, value in severity_keywords.items():
        if word in text:
            score += value

    return score

def resolution_score(hours):
    if hours <= 12:
        return 3
    elif hours <= 48:
        return 2
    else:
        return 1

def semantic_score(keyword_score):
    return min(
        1.0,
        0.4 + keyword_score * 0.08
    )

def final_severity_score(
    semantic_score,
    keyword_score,
    resolution_score
):
    return (
        0.5 * semantic_score
        + 0.3 * (keyword_score / 10)
        + 0.2 * (resolution_score / 3)
    )