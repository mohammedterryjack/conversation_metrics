from typing import Optional

from conversation_metrics.annotators.entity_extraction import EntityExtractor
from conversation_metrics.annotators.formality import Formality
from conversation_metrics.annotators.semantics import SemanticEncoder
from conversation_metrics.annotators.sentiment import Sentiment
from spacy import load
from transformers import pipeline


def customise_models(
    measure_formality: Optional[callable] = None,
    measure_sentiment: Optional[callable] = None,
    extract_entities: Optional[callable] = None,
    vectorise: Optional[callable] = None,
) -> None:
    """
    allows custom models to be used for lighter inference
        - measure_formality (text:str) -> float
        - measure_sentiment (text:str) -> float
        - extract_entities (text:str) -> List[str]
        - vectorise (text:str) -> ndarray
    """
    if measure_formality is None:
        Formality.measure = lambda _, text: Formality._measure(text)
    else:
        Formality.measure = lambda _, text: measure_formality(text)

    if measure_sentiment is None:
        Sentiment.measure = Sentiment._measure
        if Sentiment.model is None:
            Sentiment.model = pipeline(
                task="text-classification",
                model="monologg/bert-base-cased-goemotions-group",
            )
    else:
        Sentiment.measure = lambda _, text: measure_sentiment(text)

    if extract_entities is None:
        EntityExtractor.extract_entities = EntityExtractor._extract_entities
        if EntityExtractor.model is None:
            EntityExtractor.model = load(name="en_core_web_lg")
    else:
        EntityExtractor.extract_entities = lambda _, text: extract_entities(text)

    if vectorise is None:
        SemanticEncoder.vectorise = SemanticEncoder._vectorise
        if SemanticEncoder.model is None:
            SemanticEncoder.model = load(name="en_core_web_lg")
    else:
        SemanticEncoder.vectorise = lambda _, text: vectorise(text)
