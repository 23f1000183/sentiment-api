from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = FastAPI(title="Batch Sentiment API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    sentences: list[str]


def analyze_sentiment(sentence: str) -> str:
    scores = analyzer.polarity_scores(sentence)
    compound = scores["compound"]

    if compound >= 0.05:
        return "happy"
    elif compound <= -0.05:
        return "sad"
    else:
        return "neutral"


@app.post("/sentiment")
def batch_sentiment(request: SentimentRequest):
    return {
        "results": [
            {
                "sentence": sentence,
                "sentiment": analyze_sentiment(sentence),
            }
            for sentence in request.sentences
        ]
    }
