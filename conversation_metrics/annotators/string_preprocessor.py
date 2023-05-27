from conversation_metrics.utils.string_preprocessor import \
    StringPreprocessorModel


class StringPreprocessor:
    """
    a lightweight preprocessor
    for simple string manipulation
    """

    @staticmethod
    def remove_formatting(text: str) -> str:
        """
        removes capitalisations, punctuation and adds padding
        """
        return StringPreprocessorModel.PADDING.value.format(
            text=text.lower().translate(StringPreprocessorModel.TRANSLATION_TABLE.value)
        )
