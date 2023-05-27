from conversation_metrics.annotators.string_preprocessor import \
    StringPreprocessor
from conversation_metrics.models.formality_analysis import FormalityModel


class Formality:
    """
    to measure how formal (personal)
    or informal (impersonal) an utterance is
    """

    def measure(self, text: str) -> float:
        raise NotImplementedError

    @staticmethod
    def _measure(text: str) -> float:
        return float(
            not Formality.is_informal(text=StringPreprocessor().remove_formatting(text))
        )

    @staticmethod
    def is_informal(text: str) -> bool:
        return any(
            map(lambda keyword: f" {keyword} " in text, FormalityModel.KEYWORDS.value)
        )
