from unittest import TestCase, main

from conversation_metrics.annotators.entity_extraction import EntityExtractor
from conversation_metrics.annotators.formality import Formality
from conversation_metrics.annotators.semantics import SemanticEncoder
from conversation_metrics.annotators.sentiment import Sentiment
from conversation_metrics.models.custom_models import customise_models
from numpy import ndarray

customise_models()


class TestFormalityAnnotator(TestCase):
    def test_formality(self):
        annotator = Formality()
        score = annotator.measure("Barcelona is a popular tourist destination.")
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest("formal sentences produce high scores"):
            self.assertAlmostEqual(score, 1.0)
        with self.subTest("informal sentences produce low scores"):
            score = annotator.measure("We went to Barcelona for the weekend.")
            self.assertAlmostEqual(score, 0.0)


class TestSentimentAnnotator(TestCase):
    def test_sentiment(self):
        annotator = Sentiment()
        score = annotator.measure("Whatever")
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest("neutral sentiment scores are 0."):
            self.assertEqual(score, 0.0)
        with self.subTest("negative sentiment scores < 0."):
            score = annotator.measure("I hate you")
            self.assertLess(score, 0.0)
        with self.subTest("positive sentiment scores > 0."):
            score = annotator.measure("I love you")
            self.assertGreater(score, 0.0)


class TestEntityExtractor(TestCase):
    def test_entity(self):
        extractor = EntityExtractor()
        entities = extractor.extract_entities(
            text="My brother plays football but I prefer playing basketball"
        )
        with self.subTest("noun 1 (brother) extracted"):
            self.assertIn("brother", entities)
        with self.subTest("noun 2 (football) extracted"):
            self.assertIn("football", entities)
        with self.subTest("verb 1 (plays) extracted"):
            self.assertIn("plays", entities)
        with self.subTest("verb 2 (playing) extracted"):
            self.assertIn("playing", entities)
        with self.subTest("verb 3 (prefer) extracted"):
            self.assertIn("prefer", entities)
        with self.subTest("other word (My) not extracted"):
            self.assertNotIn("My", entities)
        with self.subTest("other word (but) not extracted"):
            self.assertNotIn("but", entities)
        with self.subTest("other word (I) not extracted"):
            self.assertNotIn("I", entities)


class TestSemanticEncoder(TestCase):
    def test_semantics(self):
        semantic_encoder = SemanticEncoder()
        mother = semantic_encoder.vectorise("mother")
        with self.subTest("vector is array"):
            self.assertIsInstance(mother, ndarray)


if __name__ == "__main__":
    main()
