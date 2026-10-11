from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import re

app = FastAPI(title="Batch Sentiment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: list[str]


POSITIVE_WORDS = {
    "love", "loved", "like", "liked", "great", "good", "excellent",
    "amazing", "awesome", "wonderful", "fantastic", "happy", "glad",
    "enjoy", "enjoyed", "beautiful", "perfect", "best", "brilliant",
    "delightful", "pleased", "excited", "fun", "helpful", "success",
    "successful", "impressive", "incredible", "positive", "recommend",
    "friendly", "kind", "superb", "outstanding", "favorite", "favourite",
    "grateful", "thankful", "hopeful", "satisfied", "peaceful", "proud",
    "better", "improved", "win", "won", "easy"
}

NEGATIVE_WORDS = {
    "hate", "hated", "terrible", "awful", "horrible", "bad", "worst",
    "sad", "angry", "upset", "disappointed", "disappointing", "poor",
    "boring", "annoying", "frustrating", "fail", "failed", "failure",
    "wrong", "broken", "ugly", "pain", "painful", "hurt", "unhappy",
    "miserable", "depressing", "depressed", "negative", "dislike",
    "useless", "waste", "slow", "expensive", "disgusting", "scary",
    "afraid", "lonely", "stressful", "regret", "rude", "disaster",
    "sick", "tired", "exhausted", "worse", "problem", "problems"
}

NEGATIONS = {
    "not", "never", "no", "isn't", "wasn't", "don't", "doesn't",
    "didn't", "can't", "cannot", "couldn't", "won't", "wouldn't"
}


def analyze_sentiment(sentence: str) -> str:
    words = re.findall(r"[a-z]+(?:'[a-z]+)?", sentence.lower())

    score = 0
    negate_for = 0

    for word in words:
        if word in NEGATIONS:
            negate_for = 3
            continue

        if word in POSITIVE_WORDS:
            score += -1 if negate_for else 1
            negate_for = 0
        elif word in NEGATIVE_WORDS:
            score += 1 if negate_for else -1
            negate_for = 0
        elif negate_for:
            negate_for -= 1

    if score > 0:
        return "happy"
    if score < 0:
        return "sad"
    return "neutral"


@app.post("/sentiment")
def batch_sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": analyze_sentiment(sentence)
            }
            for sentence in request.sentences
        ]
    }
