from typing import Generator, List, Optional, Tuple

from conversation_metrics.models.custom_models import customise_models
from conversation_metrics.structures.entity import Entity
from conversation_metrics.structures.settings import ConversationSettings
from conversation_metrics.structures.turn import Turn
from matplotlib.collections import LineCollection
from matplotlib.pyplot import show, subplots, text, xlabel, xlim, ylabel, ylim


class Conversation:
    """
    automatically analyses the quality of a conversation
    between a human user and an AI system
    """

    def __init__(
        self,
        conversation: Optional[str] = None,
        measure_formality: Optional[callable] = None,
        measure_sentiment: Optional[callable] = None,
        extract_entities: Optional[callable] = None,
        vectorise: Optional[callable] = None,
    ) -> None:
        customise_models(
            measure_formality=measure_formality,
            measure_sentiment=measure_sentiment,
            extract_entities=extract_entities,
            vectorise=vectorise,
        )
        self.turns: List[Turn] = list()
        self._unpaired_utterance: Optional[str] = None
        if conversation is not None:
            self._parse_text(text=conversation)

    def __repr__(self) -> str:
        return ConversationSettings.CONVERSATION_REPRESENTATION.value.format(
            border=ConversationSettings.THREAD_BORDER.value,
            turn_repreesentation=self.__represent_turns(),
            thread_representation=self.__represent_entity_threads(),
        )

    def __len__(self) -> int:
        """
        number of turns in the conversation
        """
        return len(self.turns)

    def __represent_turns(self) -> str:
        """
        displays each turn in the conversation
        """
        return ConversationSettings.TURN_CONNECTOR.value.join(map(str, self.turns))

    def __represent_entity_threads(self) -> str:
        """
        displays the linked entities discussed throughout the conversation
        to show the conversational threads
        """
        return (
            ConversationSettings.THREAD_HEADER.value
            + ConversationSettings.THREAD_HEADER.value.join(
                map(str, self._heads_of_threads())
            )
        )

    def _heads_of_threads(self) -> Generator[Entity, None, None]:
        """
        get all root entities in conversation
        which also have children linked to them
        (these are the heads of threads)
        """
        for turn in self.turns:
            for entity in turn.user.entities + turn.system.entities:
                if entity.is_thread_head():
                    yield entity

    def _parse_text(
        self,
        text: str,
        delimiter: str = ConversationSettings.UTTERANCE_DELIMITER.value,
    ) -> None:
        """
        assumptions:
            - 1: each utterance is separated by a delimiter
            - 2: successive utterances are uttered by different speakers
            - 3: there are two speakers in the conversation
            - 4: each turn must have exactly one utterance from each speaker
        """
        utterances = text.split(delimiter)
        for utterance in utterances:
            self.add_utterance(new_utterance=utterance)

    def _quality(self) -> Generator[float, None, None]:
        """
        returns turn quality scores
        for all turns in the conversation
        """
        for turn in self.turns:
            yield turn.quality

    def _tit_for_tat(self) -> Generator[float, None, None]:
        """
        returns tit-for-tat scores
        for all turns in the conversation
        """
        for turn in self.turns:
            yield turn.TfT_score

    def _inferred_reaction(self) -> Generator[float, None, None]:
        """
        returns inferred reaction scores
        for all turns in the conversation
        """
        for turn in self.turns:
            yield turn.R_score

    def _sentiment(self) -> Generator[float, None, None]:
        """
        returns sentiment scores
        for all utterances in the conversation
        assumption: user starts the turn
        """
        for turn in self.turns:
            yield turn.user.sentiment
            yield turn.system.sentiment

    def _formality(self) -> Generator[float, None, None]:
        """
        returns formality scores
        for all utterances in the conversation
        assumption: user starts the turn
        """
        for turn in self.turns:
            yield turn.user.formality
            yield turn.system.formality

    def _turn_index(self) -> Generator[int, None, None]:
        """
        returns index for all turns in the conversation
        """
        for turn in self.turns:
            yield turn.index * ConversationSettings.TURN_UTTERANCE_ALIGNMENT_FACTOR.value

    def _utterance_index(self) -> Generator[int, None, None]:
        """
        returns index for all utterances in the conversation
        """
        for turn in self.turns:
            yield turn.user.index
            yield turn.system.index

    def _link_coordinates(
        self,
    ) -> Generator[Tuple[Tuple[float, float], Tuple[float, float]], None, None]:
        """
        return all the coordinates for lines/segments
        which link two entities in a thread
        """
        for turn in self.turns:
            for entity in turn.user.entities + turn.system.entities:
                if entity.is_linked():
                    entity_coordinates = (entity.x, entity.y)
                    for child in entity._children:
                        child_coordinates = (child.x, child.y)
                        yield entity_coordinates, child_coordinates

    def _link_widths(self) -> Generator[float, None, None]:
        """
        return all widths for lines which link two entities in a thread
        the widths are based on the entities' semantic similarities
        """
        for turn in self.turns:
            for entity in turn.user.entities + turn.system.entities:
                if entity.is_linked():
                    for child in entity._children:
                        yield child._parent_similarity * ConversationSettings.LINK_WIDTH.value

    def add_utterance(self, new_utterance: str) -> None:
        """
        adds a new utterance into the conversation
        only updates after receiving both a user and system utterance
        Note: turn indexes begin from 1 (not 0)
        """
        if self._unpaired_utterance is None:
            self._unpaired_utterance = new_utterance
            return

        new_turn = Turn(
            index=len(self) + ConversationSettings.TURN_START_OFFSET.value,
            user_utterance=self._unpaired_utterance,
            system_utterance=new_utterance,
        )

        if any(self.turns):
            self.turns[-1].link_next_turn(next_turn=new_turn)
        self.turns.append(new_turn)
        self._unpaired_utterance = None

    def display_scores(self, path_to_save_image: Optional[str] = None) -> None:
        """
        plots the turn quality over time
        as well as the Tit-for-tat and Reaction scores overlaid
        """
        turns = list(self._turn_index())
        utterance_ids = list(self._utterance_index())
        quality = list(self._quality())
        tft_score = list(self._tit_for_tat())
        r_score = list(self._inferred_reaction())
        sentiment = list(self._sentiment())
        formality = list(self._formality())

        figure, graphs = subplots(
            nrows=ConversationSettings.SCORES_NUMBER_OF_GRAPHS.value, sharex=True
        )
        top_graph, bottom_graph = graphs
        figure.suptitle(ConversationSettings.SCORES_TITLE.value)
        bottom_graph.set_xlabel(ConversationSettings.SCORES_X_LABEL.value)

        top_graph.plot(
            turns,
            quality,
            alpha=ConversationSettings.SCORES_LINE_STRENGTH.value,
            label=ConversationSettings.QUALITY_LABEL.value,
        )
        top_graph.plot(
            turns,
            tft_score,
            alpha=ConversationSettings.SCORES_LINE_STRENGTH.value,
            label=ConversationSettings.TIT_FOR_TAT_LABEL.value,
        )
        top_graph.plot(
            turns,
            r_score,
            alpha=ConversationSettings.SCORES_LINE_STRENGTH.value,
            label=ConversationSettings.INFERRED_REACTION_LABEL.value,
        )
        bottom_graph.plot(
            utterance_ids,
            sentiment,
            alpha=ConversationSettings.SCORES_LINE_STRENGTH.value,
            label=ConversationSettings.SENTIMENT_LABEL.value,
            color=ConversationSettings.SENTIMENT_COLOUR.value,
        )
        bottom_graph.plot(
            utterance_ids,
            formality,
            alpha=ConversationSettings.SCORES_LINE_STRENGTH.value,
            label=ConversationSettings.FORMALITY_LABEL.value,
            color=ConversationSettings.FORMALITY_COLOUR.value,
        )
        top_graph.legend()
        bottom_graph.legend()

        show()
        if path_to_save_image is not None:
            figure.savefig(path_to_save_image)

    def display_threads(self, path_to_save_image: Optional[str] = None) -> None:
        """
        plots the entities discussed throughout the conversation
        to show the conversational threads
        """
        figure, axes = subplots()
        lines = LineCollection(
            self._link_coordinates(),
            colors=ConversationSettings.LINK_COLOUR.value,
            linewidths=list(self._link_widths()),
        )
        axes.add_collection(lines)
        conversation_depth = -len(list(self._utterance_index()))
        ylim(conversation_depth, ConversationSettings.THREADS_MAXIMUM_Y.value)
        xlim(
            ConversationSettings.THREADS_MINIMUM_X.value,
            ConversationSettings.THREADS_MAXIMUM_X.value,
        )
        ylabel(ConversationSettings.THREADS_Y_LABEL.value)
        xlabel(ConversationSettings.THREADS_X_LABEL.value)
        text(
            ConversationSettings.LEGEND_USER_LABEL_Y_COORDINATE.value,
            ConversationSettings.LEGEND_USER_LABEL_X_COORDINATE.value,
            ConversationSettings.USER_LABEL.value,
            color=ConversationSettings.USER_TEXT_COLOUR.value,
            bbox=ConversationSettings.USER_BOUNDING_BOX.value,
        )
        text(
            ConversationSettings.LEGEND_SYSTEM_LABEL_Y_COORDINATE.value,
            ConversationSettings.LEGEND_SYSTEM_LABEL_X_COORDINATE.value,
            ConversationSettings.SYSTEM_LABEL.value,
            color=ConversationSettings.SYSTEM_TEXT_COLOUR.value,
            bbox=ConversationSettings.SYSTEM_BOUNDING_BOX.value,
        )
        for turn in self.turns:
            for entity in turn.user.entities:
                if not entity.is_stub():
                    text(
                        entity.x,
                        entity.y,
                        entity.text,
                        color=ConversationSettings.USER_TEXT_COLOUR.value,
                        bbox=ConversationSettings.USER_BOUNDING_BOX.value,
                    )
            for entity in turn.system.entities:
                if not entity.is_stub():
                    text(
                        entity.x,
                        entity.y,
                        entity.text,
                        color=ConversationSettings.SYSTEM_TEXT_COLOUR.value,
                        bbox=ConversationSettings.SYSTEM_BOUNDING_BOX.value,
                    )
        show()
        if path_to_save_image is not None:
            figure.savefig(path_to_save_image)
