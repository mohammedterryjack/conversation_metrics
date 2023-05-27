from unittest import TestCase, main

from conversation_metrics.metrics.inferred_reaction import InferredReaction
from conversation_metrics.metrics.tit_for_tat import TitForTat
from conversation_metrics.metrics.turn_quality import TurnQuality
from conversation_metrics.metrics.utils import (reaction, reciprocation,
                                                weighted_average)


class TestTurnQuality(TestCase):
    def test_measure(self):
        score = TurnQuality().measure(
            tit_for_tat_score=0.5, inferred_reaction_score=0.5
        )
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"0. <= {score}"):
            self.assertGreaterEqual(score, 0.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)


class TestInferredReaction(TestCase):
    def test_measure(self):
        score = InferredReaction().measure(
            formality_prior=0.5,
            formality_after=0.5,
            sentiment_prior=0.5,
            sentiment_after=0.5,
            mean_semantic_overlap=0.5,
        )
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"0. <= {score}"):
            self.assertGreaterEqual(score, 0.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)

    def test_sentiment_reaction(self):
        score = InferredReaction()._sentiment_reaction(
            sentiment_prior=0.5, sentiment_after=0.5
        )
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"-1. <= {score}"):
            self.assertGreaterEqual(score, -1.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        with self.subTest(f"Increased Sentiment -> Positive Reaction"):
            score = InferredReaction()._sentiment_reaction(
                sentiment_prior=-0.5, sentiment_after=0.5
            )
            self.assertGreater(score, 0.0)
        with self.subTest(f"Decreased Sentiment -> Negative Reaction"):
            score = InferredReaction()._sentiment_reaction(
                sentiment_prior=0.5, sentiment_after=-0.5
            )
            self.assertLess(score, 0.0)
        with self.subTest(f"Same Sentiment -> No Reaction"):
            score = InferredReaction()._sentiment_reaction(
                sentiment_prior=0.5, sentiment_after=0.5
            )
            self.assertEqual(score, 0.0)

    def test_formality_reaction(self):
        score = InferredReaction()._formality_reaction(
            formality_prior=0.5, formality_after=0.5
        )
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"-1. <= {score}"):
            self.assertGreaterEqual(score, -1.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        with self.subTest(f"Increased Formality -> Negative Reaction"):
            score = InferredReaction()._formality_reaction(
                formality_prior=-0.5, formality_after=0.5
            )
            self.assertLess(score, 0.0)
        with self.subTest(f"Decreased Formality -> Positive Reaction"):
            score = InferredReaction()._formality_reaction(
                formality_prior=0.5, formality_after=-0.5
            )
            self.assertGreater(score, 0.0)
        with self.subTest(f"Same Formality -> No Reaction"):
            score = InferredReaction()._formality_reaction(
                formality_prior=0.5, formality_after=0.5
            )
            self.assertEqual(score, 0.0)

    def test_entity_reaction(self):
        score = InferredReaction()._entity_reaction(mean_semantic_overlap=0.5)
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"-1. <= {score}"):
            self.assertGreaterEqual(score, -1.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        with self.subTest(f"High Overlap -> Positive Reaction"):
            score = InferredReaction()._entity_reaction(mean_semantic_overlap=1.0)
            self.assertGreater(score, 0.0)
        with self.subTest(f"Low Overlap -> Negative Reaction"):
            score = InferredReaction()._entity_reaction(mean_semantic_overlap=0.0)
            self.assertLess(score, 0.0)
        with self.subTest(f"Medium Overlap -> No Reaction"):
            score = InferredReaction()._entity_reaction(mean_semantic_overlap=0.5)
            self.assertEqual(score, 0.0)


class TestTitForTat(TestCase):
    def test_measure(self):
        score = TitForTat().measure(
            formality_prior=0.5,
            formality_after=0.5,
            sentiment_prior=0.5,
            sentiment_after=0.5,
            mean_semantic_overlap=0.5,
        )
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"-1. <= {score}"):
            self.assertGreaterEqual(score, -1.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)

    def test_sentiment_reciprocation(self):
        score = TitForTat()._sentiment_reciprocation(
            sentiment_prior=0.5, sentiment_after=0.5
        )
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"0. <= {score}"):
            self.assertGreaterEqual(score, 0.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        with self.subTest(f"Increased Sentiment -> Low Reciprocation"):
            score = TitForTat()._sentiment_reciprocation(
                sentiment_prior=-0.5, sentiment_after=0.5
            )
            self.assertNotAlmostEqual(score, 0.1)
        with self.subTest(f"Decreased Sentiment -> Low Reciprocation"):
            score = TitForTat()._sentiment_reciprocation(
                sentiment_prior=0.5, sentiment_after=-0.5
            )
            self.assertNotAlmostEqual(score, 0.1)
        with self.subTest(f"Same Sentiment -> High Reciprocation"):
            score = TitForTat()._sentiment_reciprocation(
                sentiment_prior=0.5, sentiment_after=0.5
            )
            self.assertEqual(score, 1.0)

    def test_formality_reciprocation(self):
        score = TitForTat()._formality_reciprocation(
            formality_prior=0.5, formality_after=0.5
        )
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"0. <= {score}"):
            self.assertGreaterEqual(score, 0.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        with self.subTest(f"Increased Formality -> Low Reciprocation"):
            score = TitForTat()._formality_reciprocation(
                formality_prior=-0.5, formality_after=0.5
            )
            self.assertNotAlmostEqual(score, 0.1)
        with self.subTest(f"Decreased Formality -> Low Reciprocation"):
            score = TitForTat()._formality_reciprocation(
                formality_prior=0.5, formality_after=-0.5
            )
            self.assertNotAlmostEqual(score, 0.1)
        with self.subTest(f"Same Formality -> High Reciprocation"):
            score = TitForTat()._formality_reciprocation(
                formality_prior=0.5, formality_after=0.5
            )
            self.assertEqual(score, 1.0)

    def test_entity_reciprocation(self):
        score = TitForTat()._entity_reciprocation(mean_semantic_overlap=0.5)
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"0. <= {score}"):
            self.assertGreaterEqual(score, 0.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        with self.subTest(f"High Overlap -> High Reciprocation"):
            score = TitForTat()._entity_reciprocation(mean_semantic_overlap=1.0)
            self.assertEqual(score, 1.0)
        with self.subTest(f"Low Overlap -> Low Reciprocation"):
            score = TitForTat()._entity_reciprocation(mean_semantic_overlap=0.0)
            self.assertEqual(score, 0.0)
        with self.subTest(f"Medium Overlap -> Medium Reciprocation"):
            score = TitForTat()._entity_reciprocation(mean_semantic_overlap=0.5)
            self.assertEqual(score, 0.5)


class TestMetricUtils(TestCase):
    def test_weighted_average(self):
        score = weighted_average(values=[10, 20, 30], weights=[1.0, 1.0, 1.0])
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest("Equal Weights"):
            score = weighted_average(values=[10, 20, 30], weights=[1.0, 1.0, 1.0])
            self.assertEqual(score, 20.0)
        with self.subTest("Biased Weights"):
            score = weighted_average(values=[10, 20, 30], weights=[0.0, 0.0, 1.0])
            self.assertEqual(score, 10.0)
        with self.subTest("All Inhibiting Weights"):
            score = weighted_average(values=[10, 20, 30], weights=[0.0, 0.0, 0.0])
            self.assertEqual(score, 0.0)

    def test_reaction(self):
        score = reaction(score_a=0.5, score_b=0.5)
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"-1. <= {score}"):
            self.assertGreaterEqual(score, -1.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)

    def test_reciprocation(self):
        score = reciprocation(score_a=0.5, score_b=0.5)
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"-1. <= {score}"):
            self.assertGreaterEqual(score, -1.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)

    def test_reaction_and_reciprocation_relationship(self):
        with self.subTest("Positive Reaction -> Low Reciprocation"):
            score_a, score_b = -1.0, 1.0
            score1 = reaction(score_a, score_b)
            score2 = reciprocation(score_a, score_b)
            self.assertGreater(score1, 0.0)
            self.assertLess(score2, 0.5)
        with self.subTest("Negative Reaction -> Low Reciprocation"):
            score_a, score_b = 1.0, -1.0
            score1 = reaction(score_a, score_b)
            score2 = reciprocation(score_a, score_b)
            self.assertLess(score1, 0.0)
            self.assertLess(score2, 0.5)
        with self.subTest("No Reaction -> High Reciprocation"):
            score_a, score_b = 1.0, 1.0
            score1 = reaction(score_a, score_b)
            score2 = reciprocation(score_a, score_b)
            self.assertEqual(score1, 0.0)
            self.assertEqual(score2, 1.0)


if __name__ == "__main__":
    main()
