from typing import Generator, Optional

from conversation_metrics.annotators.entity_extraction import EntityExtractor
from conversation_metrics.annotators.formality import Formality
from conversation_metrics.annotators.sentiment import Sentiment
from conversation_metrics.annotators.string_preprocessor import \
    StringPreprocessor
from conversation_metrics.structures.entity import Entity
from conversation_metrics.structures.settings import ConversationSettings


class Utterance:
    def __init__(
        self,
        text: str,
        utterance_index: int,
        minimum_similarity_to_link_entities: float = ConversationSettings.LINK_SIMILARITY_THRESHOLD.value,
    ) -> None:
        self.index = utterance_index
        self.entity_linking_threshold = minimum_similarity_to_link_entities
        self.sentiment = self._measure_sentiment(text)
        self.formality = self._measure_formality(text)
        self.entities = list(self._extract_entities(text, self.index))
        self.text = text
        self._entities_in_text = self._highlight_entities(
            text=StringPreprocessor().remove_formatting(text)
        )

    def __repr__(self) -> str:
        return ConversationSettings.UTTERANCE_REPRESENTATION.value.format(
            utterance=self._entities_in_text,
            sentiment_label=ConversationSettings.SENTIMENT_LABEL.value,
            formality_label=ConversationSettings.FORMALITY_LABEL.value,
            sentiment_score=round(self.sentiment, ConversationSettings.ROUND_TO.value),
            formality_score=round(self.formality, ConversationSettings.ROUND_TO.value),
        )

    def mean_semantic_overlap(self, other: "Utterance") -> float:
        """
        the percentage of the entities in common with some other utterance
        matches are based on the semantics of the entity (not the string)
        """
        if not any(self.entities):
            return ConversationSettings.MAX_OVERLAP_SCORE.value

        if not any(other.entities):
            return ConversationSettings.MIN_OVERLAP_SCORE.value

        total_semantic_overlap = ConversationSettings.MIN_OVERLAP_SCORE.value
        for entity in self.entities:
            entity.link(
                others=other.entities,
                similarity_threshold=self.entity_linking_threshold,
            )
            most_similar_entity = max(
                other.entities, key=lambda child: child._parent_similarity
            )
            total_semantic_overlap += most_similar_entity._parent_similarity

        return total_semantic_overlap / len(self.entities)

    def _highlight_entities(self, text: str) -> str:
        """
        format the STRING so that
        all ENTITIES are highlighted
        """
        for entity in self.entities:
            text = text.replace(f" {entity.text.lower()} ", f" {entity.text.upper()} ")
        return text

    @staticmethod
    def _measure_sentiment(text: str) -> float:
        return (
            Sentiment().measure(text)
            * ConversationSettings.SENTIMENT_NORMALISATION_FACTOR.value
        )

    @staticmethod
    def _measure_formality(text: str) -> float:
        return Formality().measure(text)

    @staticmethod
    def _extract_entities(
        text: str, utterance_index: int
    ) -> Generator[Entity, None, None]:
        for entity in EntityExtractor().extract_entities(text):
            yield Entity(entity, utterance_index)
