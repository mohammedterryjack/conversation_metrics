from conversation_metrics.metrics.utils import MetricDefaults, weighted_average


class TurnQuality:
    """
    a score indicating the level of quality
    of a conversational turn
    based on signals derived from the interaction
    between the user and system
    """

    def __init__(
        self,
        tit_for_tat_influence=MetricDefaults.WEIGHT.value,
        inferred_reaction_influence=MetricDefaults.WEIGHT.value,
    ) -> None:
        self.weight_TfT = tit_for_tat_influence
        self.weight_R = inferred_reaction_influence

    def measure(
        self, tit_for_tat_score: float, inferred_reaction_score: float
    ) -> float:
        return weighted_average(
            values=(tit_for_tat_score, inferred_reaction_score),
            weights=(self.weight_TfT, self.weight_R),
        )
