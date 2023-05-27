from unittest import TestCase, main

from conversation_metrics import evaluate_replies, select_highest_quality_reply
from conversation_metrics.utils.rank_and_select import evaluate_reply

EXAMPLE_UTTERANCE = "this is a lovely test"
BEST_REPLY = "what's so lovely about this test"
EXAMPLE_CANDIDATES = [BEST_REPLY, "how do you know", "bla bla", "what do you mean?"]


class TestEvaluateUtils(TestCase):
    def test_evaluate_reply(self):
        with self.subTest("test normal behaviour"):
            quality = evaluate_reply(utterance=EXAMPLE_UTTERANCE, reply="thanks")
            self.assertIsInstance(quality, float)
            self.assertGreaterEqual(quality, -1.0)
            self.assertLessEqual(quality, 1.0)

        with self.subTest("test null reply doesnt break it"):
            quality = evaluate_reply(utterance=EXAMPLE_UTTERANCE, reply=None)
            self.assertIsInstance(quality, float)
            self.assertGreaterEqual(quality, -1.0)
            self.assertLessEqual(quality, 1.0)

    def test_evaluate_replies(self):
        with self.subTest("test normal behaviour"):
            qualities = list(
                evaluate_replies(
                    utterance=EXAMPLE_UTTERANCE,
                    replies=EXAMPLE_CANDIDATES,
                )
            )
            self.assertIsInstance(qualities, list)
            self.assertIsInstance(sum(qualities), float)

    def test_select_highest_quality_reply(self):
        with self.subTest("test normal behaviour"):
            selected_reply = select_highest_quality_reply(
                utterance=EXAMPLE_UTTERANCE,
                replies=EXAMPLE_CANDIDATES,
            )
            self.assertIsInstance(selected_reply, str)
            self.assertEqual(selected_reply, BEST_REPLY)


if __name__ == "__main__":
    main()
