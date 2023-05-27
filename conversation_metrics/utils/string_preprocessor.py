from enum import Enum
from string import punctuation


class StringPreprocessorModel(Enum):
    PADDING = " {text} "
    TRANSLATION_TABLE = "".maketrans(punctuation, " " * len(punctuation))
