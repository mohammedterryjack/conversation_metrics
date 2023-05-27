from typing import List

from conversation_metrics.metrics.utils import (MetricDefaults, reaction,
                                                weighted_average)


class InferredReaction:
    """
    the user's apparent reaction to the system's utterance
    inferred from changes in their sentiment, formality, etc
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
        return weighted_average(
            values=(
                self._formality_reaction(
                    formality_prior=formality_prior,
                    formality_after=formality_after,
                ),
                self._sentiment_reaction(
                    sentiment_prior=sentiment_prior,
                    sentiment_after=sentiment_after,
                ),
                self._entity_reaction(mean_semantic_overlap),
            ),
            weights=(self.weight_formality, self.weight_sentiment, self.weight_entity),
        )

    @staticmethod
    def _sentiment_reaction(sentiment_prior: float, sentiment_after: float) -> float:
        return reaction(sentiment_prior, sentiment_after)

    @staticmethod
    def _formality_reaction(formality_prior: float, formality_after: float) -> float:
        return -reaction(formality_prior, formality_after)

    @staticmethod
    def _entity_reaction(mean_semantic_overlap: float) -> float:
        return 2 * mean_semantic_overlap - 1
