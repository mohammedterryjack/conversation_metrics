from typing import Generator, List

from conversation_metrics.models.entity_extraction import EntityModel


class EntityExtractor:
    """
    to extract the words in the utterance
    which carry the most meaning
    (i.e. the nouns and verbs)
    """

    model = None

    def extract_entities(self, text: str) -> List[str]:
        raise NotImplementedError

    def _extract_entities(self, text: str) -> List[str]:
        return list(self._root_nouns_from_noun_chunks(text)) + list(self._verbs(text))

    def _root_nouns_from_noun_chunks(self, text: str) -> Generator[str, None, None]:
        """
        splits text into noun chunks
        and extracts the root noun from each chunk
        and any nouns attached to that
        """
        for noun_chunk in self.model(text).noun_chunks:
            if self.is_noun(part_of_speech_tag=noun_chunk.root.pos_):
                yield noun_chunk.root.text

            for token in noun_chunk.root.children:
                if self.is_noun(part_of_speech_tag=token.pos_):
                    yield token.text

    def _verbs(self, text: str) -> Generator[str, None, None]:
        """
        extracts all verbs
        """
        for token in self.model(text):
            if self.is_verb(part_of_speech_tag=token.pos_):
                yield token.text

    @staticmethod
    def is_noun(part_of_speech_tag: str) -> bool:
        return part_of_speech_tag in (
            EntityModel.NOUN.value,
            EntityModel.PROPER_NOUN.value,
        )

    @staticmethod
    def is_verb(part_of_speech_tag: str) -> bool:
        return part_of_speech_tag == EntityModel.VERB.value
