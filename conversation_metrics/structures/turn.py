from typing import Optional

from conversation_metrics.metrics.inferred_reaction import InferredReaction
from conversation_metrics.metrics.tit_for_tat import TitForTat
from conversation_metrics.metrics.turn_quality import TurnQuality
from conversation_metrics.structures.settings import ConversationSettings
from conversation_metrics.structures.utterance import Utterance


class Turn:
    def __init__(
        self,
        index: int,
        user_utterance: str,
        system_utterance: str,
    ) -> None:

        self.index = index
        utterance_index = (
            index * ConversationSettings.TURN_UTTERANCE_ALIGNMENT_FACTOR.value
        )
        self.user = Utterance(
            text=user_utterance,
            utterance_index=utterance_index - 1,
        )
        self.system = Utterance(
            text=system_utterance,
            utterance_index=utterance_index,
        )
        self.TfT_score = TitForTat().measure(
            formality_prior=self.user.formality,
            formality_after=self.system.formality,
            sentiment_prior=self.user.sentiment,
            sentiment_after=self.system.sentiment,
            mean_semantic_overlap=self.user.mean_semantic_overlap(other=self.system),
        )
        self.link_next_turn(next_turn=None)

    def __repr__(self) -> str:
        return ConversationSettings.TURN_REPRESENTATION.value.format(
            border=ConversationSettings.TURN_BORNER.value,
            turn_label=ConversationSettings.TURN_LABEL.value,
            user_label=ConversationSettings.USER_LABEL.value,
            system_label=ConversationSettings.SYSTEM_LABEL.value,
            quality_label=ConversationSettings.QUALITY_LABEL.value,
            tft_label=ConversationSettings.TIT_FOR_TAT_LABEL.value,
            r_label=ConversationSettings.INFERRED_REACTION_LABEL.value,
            turn_number=self.index,
            user_utterance=self.user,
            system_utterance=self.system,
            quality_score=round(self.quality, ConversationSettings.ROUND_TO.value),
            tft_score=round(self.TfT_score, ConversationSettings.ROUND_TO.value),
            r_score=ConversationSettings.SCORE_PLACEHOLDER.value
            if self.R_score is None
            else round(self.R_score, ConversationSettings.ROUND_TO.value),
        )

    def link_next_turn(self, next_turn: Optional["Turn"]) -> None:
        """
        if there is no next turn yet
        there is no way to calculate the user's reaction (R-score)
        and so the turn's quality is equivalent to the TfT score
        otherwise, the turn's Quality is calculated via both;
        (i.e. the weighted average of TfT and R scores)
        """
        self.next = next_turn

        if self.next is None:
            self.R_score = None
            self.quality = self.TfT_score
            return

        self.R_score = InferredReaction().measure(
            sentiment_prior=self.system.sentiment,
            sentiment_after=self.next.user.sentiment,
            formality_prior=self.system.formality,
            formality_after=self.next.user.formality,
            mean_semantic_overlap=self.system.mean_semantic_overlap(
                other=self.next.user
            ),
        )
        self.quality = TurnQuality().measure(
            tit_for_tat_score=self.TfT_score, inferred_reaction_score=self.R_score
        )
