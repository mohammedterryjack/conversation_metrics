from typing import Generator, List, Optional

from conversation_metrics.structures.conversation import Conversation


def evaluate_reply(
    utterance: str,
    reply: Optional[str],
    measure_formality: Optional[callable] = None,
    measure_sentiment: Optional[callable] = None,
    extract_entities: Optional[callable] = None,
    vectorise: Optional[callable] = None,
) -> float:
    """
    use the conversation metric to evaluate the quality of a single response
    """
    if reply is None:
        return -1.0
    metric = Conversation(
        measure_formality=measure_formality,
        measure_sentiment=measure_sentiment,
        extract_entities=extract_entities,
        vectorise=vectorise,
    )
    metric.add_utterance(new_utterance=utterance)
    metric.add_utterance(new_utterance=reply)
    results = list(metric._quality())
    return results[-1]


def evaluate_replies(
    utterance: str,
    replies: List[str],
    measure_formality: Optional[callable] = None,
    measure_sentiment: Optional[callable] = None,
    extract_entities: Optional[callable] = None,
    vectorise: Optional[callable] = None,
) -> Generator[float, None, None]:
    """
    measures the conversation quality of each candidate reply
    """
    for reply in replies:
        yield evaluate_reply(
            utterance=utterance,
            reply=reply,
            measure_formality=measure_formality,
            measure_sentiment=measure_sentiment,
            extract_entities=extract_entities,
            vectorise=vectorise,
        )


def select_highest_quality_reply(
    utterance: str,
    replies: List[str],
    measure_formality: Optional[callable] = None,
    measure_sentiment: Optional[callable] = None,
    extract_entities: Optional[callable] = None,
    vectorise: Optional[callable] = None,
) -> str:
    """
    selects best reply to the utterance
    based on the measured qualities
    """
    qualities = list(
        evaluate_replies(
            utterance=utterance,
            replies=replies,
            measure_formality=measure_formality,
            measure_sentiment=measure_sentiment,
            extract_entities=extract_entities,
            vectorise=vectorise,
        )
    )
    best_quality = max(qualities)
    best_index = qualities.index(best_quality)
    return replies[best_index]
