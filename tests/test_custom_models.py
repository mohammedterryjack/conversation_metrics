from unittest import TestCase, main

from conversation_metrics.utils.rank_and_select import \
    select_highest_quality_reply

BAD_ANNOTATORS_REPLY = "how do you know"
GOOD_ANNOTATORS_REPLY = "what's so lovely about this test"
EXAMPLE_REPLIES = [
    BAD_ANNOTATORS_REPLY,
    GOOD_ANNOTATORS_REPLY,
    "what do you mean?",
]


class TestModelCustomisation(TestCase):
    def test_load_custom_models(self):
        reply = select_highest_quality_reply(
            utterance="this is a lovely test",
            replies=EXAMPLE_REPLIES,
            measure_formality=lambda text: 1.0,
            measure_sentiment=lambda text: -1.0,
            extract_entities=lambda text: ["entity1", "entity2"],
            vectorise=lambda entity: [0.2, -0.9, 0.5],
        )
        self.assertEqual(reply, BAD_ANNOTATORS_REPLY)

    def test_reload_with_default_models(self):
        reply = select_highest_quality_reply(
            utterance="this is a lovely test",
            replies=EXAMPLE_REPLIES,
        )
        self.assertEqual(reply, GOOD_ANNOTATORS_REPLY)

    def test_reload_with_custom_models(self):
        reply = select_highest_quality_reply(
            utterance="this is a lovely test",
            replies=EXAMPLE_REPLIES,
            measure_formality=lambda text: 1.0,
            measure_sentiment=lambda text: -1.0,
            extract_entities=lambda text: ["entity1", "entity2"],
            vectorise=lambda entity: [0.2, -0.9, 0.5],
        )
        self.assertEqual(reply, BAD_ANNOTATORS_REPLY)
