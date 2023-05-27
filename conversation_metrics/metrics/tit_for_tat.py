from typing import List

from conversation_metrics.metrics.utils import (MetricDefaults, reciprocation,
                                                weighted_average)
from conversation_metrics.structures.entity import Entity


class TitForTat:
    """
    the system's level of reciprocation
    to the user's sentiment, formality and entities
    (each taken into consideration equally by default)
    """

    def __init__(
        self,
        formality_influence: float = MetricDefaults.WEIGHT.value,
        sentiment_influence: float = MetricDefaults.WEIGHT.value,
        entity_influence: float = MetricDefaults.WEIGHT.value,
    ) -> None:
        self.weight_formality = formality_influence
        self.weight_sentiment = sentiment_influence
        self.weight_entity = entity_influence

    def measure(
        self,
        formality_prior: float,
        formality_after: float,
        sentiment_prior: float,
        sentiment_after: float,
        mean_semantic_overlap: float,
    ) -> float:
        score = weighted_average(
            values=(
                self._formality_reciprocation(
                    formality_prior=formality_prior,
                    formality_after=formality_after,
                ),
                self._sentiment_reciprocation(
                    sentiment_prior=sentiment_prior,
                    sentiment_after=sentiment_after,
                ),
                self._entity_reciprocation(mean_semantic_overlap),
            ),
            weights=(
                self.weight_formality,
                self.weight_sentiment,
                self.weight_entity,
            ),
        )
        return 2 * score - 1

    @staticmethod
    def _sentiment_reciprocation(
        sentiment_prior: float, sentiment_after: float
    ) -> float:
        return reciprocation(sentiment_prior, sentiment_after)

    @staticmethod
    def _formality_reciprocation(
        formality_prior: float, formality_after: float
    ) -> float:
        return reciprocation(formality_prior, formality_after)

    @staticmethod
    def _entity_reciprocation(mean_semantic_overlap: float) -> float:
        return mean_semantic_overlap
