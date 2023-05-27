from numpy import ndarray


class SemanticEncoder:
    """
    to encode the semantics of text
    """

    model = None

    def vectorise(self, text: str) -> ndarray:
        raise NotImplementedError

    def _vectorise(self, text: str) -> ndarray:
        return self.model(text).vector
