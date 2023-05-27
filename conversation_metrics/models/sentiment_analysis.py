from enum import Enum


class SentimentModel(Enum):
    NEUTRAL = "neutral"
    POSITIVE = "positive"
    NEGATIVE = "negative"
    SCORE = "score"
    LABEL = "label"
