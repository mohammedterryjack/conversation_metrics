from typing import Tuple

from conversation_metrics.models.sentiment_analysis import SentimentModel


class Sentiment:
    """
    to measure the positivity/negativity/neutrality
    of a given utterance
    """

    model = None

    def measure(self, text: str) -> float:
        raise NotImplementedError

    def _measure(self, text: str) -> float:
        label, score = self._predict_label_and_score(text)
        if label.lower() == SentimentModel.POSITIVE.value:
            return score
        elif label.lower() == SentimentModel.NEGATIVE.value:
            return -score
        else:
            return 0.0

    def _predict_label_and_score(self, text: str) -> Tuple[str, float]:
        result = self.model(text)[0]
        label, score = (
            result[SentimentModel.LABEL.value],
            result[SentimentModel.SCORE.value],
        )
        return label, score
