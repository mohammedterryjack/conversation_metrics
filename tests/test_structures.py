from unittest import TestCase, main

from conversation_metrics.structures.conversation import Conversation
from conversation_metrics.structures.entity import Entity
from conversation_metrics.structures.turn import Turn
from conversation_metrics.structures.utterance import Utterance
from numpy import ndarray

EXAMPLE_CONVERSATION_ABOUT_CATS = """i like cats
cats are so cute. do you have any?
no. we used to have two kittens
aww. what happened to them? why don't you still have them?
we had to give them away because my mum was allergic
oh thats a shame. I'm sorry to hear that"""
NUMBER_OF_TURNS_IN_CAT_EXAMPLE = 3
NUMBER_OF_UTTERANCES_IN_CAT_EXAMPLE = 6


class TestConversation(TestCase):
    def test_init(self):
        with self.subTest("instantiating without any input"):
            Conversation()
        with self.subTest("instantiating with a string"):
            Conversation(conversation=EXAMPLE_CONVERSATION_ABOUT_CATS)

    def test_respresentations(self):
        example_conversation = Conversation(
            conversation=EXAMPLE_CONVERSATION_ABOUT_CATS
        )
        self.assertIsInstance(str(example_conversation), str)

    def test_len(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        self.assertEqual(len(example_conversation), NUMBER_OF_TURNS_IN_CAT_EXAMPLE)

    def test_parse_text(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        self.assertTrue(any(example_conversation.turns))

    def test_quality(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        scores = list(example_conversation._quality())
        self.assertEqual(len(scores), NUMBER_OF_TURNS_IN_CAT_EXAMPLE)

    def test_tit_for_tat(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        scores = list(example_conversation._tit_for_tat())
        self.assertEqual(len(scores), NUMBER_OF_TURNS_IN_CAT_EXAMPLE)

    def test_inferred_reaction(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        scores = list(example_conversation._inferred_reaction())
        self.assertEqual(len(scores), NUMBER_OF_TURNS_IN_CAT_EXAMPLE)

    def test_sentiment(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        scores = list(example_conversation._sentiment())
        self.assertEqual(len(scores), NUMBER_OF_UTTERANCES_IN_CAT_EXAMPLE)

    def test_formality(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        scores = list(example_conversation._formality())
        self.assertEqual(len(scores), NUMBER_OF_UTTERANCES_IN_CAT_EXAMPLE)

    def test_turn_index(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        indexes = list(example_conversation._turn_index())
        self.assertEqual(len(indexes), NUMBER_OF_TURNS_IN_CAT_EXAMPLE)

    def test_utterance_index(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        indexes = list(example_conversation._utterance_index())
        self.assertEqual(len(indexes), NUMBER_OF_UTTERANCES_IN_CAT_EXAMPLE)

    def test_add_utterance(self):
        example_conversation = Conversation()
        number_of_turns_before = len(example_conversation)
        with self.subTest("adding one utterance doesnt increase number of turns"):
            example_conversation.add_utterance(new_utterance="foo")
            number_of_turns_after = len(example_conversation)
            self.assertEqual(number_of_turns_before, number_of_turns_after)
        with self.subTest("adding a pair of utterances does increase number of turns"):
            example_conversation.add_utterance(new_utterance="bar")
            number_of_turns_after = len(example_conversation)
            self.assertEqual(number_of_turns_before, number_of_turns_after - 1)

    def test_display_scores(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        example_conversation.display_scores()

    def test_display_threads(self):
        example_conversation = Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)
        example_conversation.display_threads()

    def test_link_coordinates(self):
        Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)._link_coordinates()

    def test_heads_of_threads(self):
        Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)._heads_of_threads()

    def test_link_widths(self):
        Conversation(EXAMPLE_CONVERSATION_ABOUT_CATS)._link_widths()


class TestTurn(TestCase):
    def test_init(self):
        example_turn = Turn(
            index=0, user_utterance="hiya Bob", system_utterance="heya Harry. whats up?"
        )
        with self.subTest("index set"):
            self.assertEqual(example_turn.index, 0)
        with self.subTest("TfT score set"):
            self.assertIsInstance(example_turn.TfT_score, float)
        with self.subTest("R score set to None"):
            self.assertIsNone(example_turn.R_score)
        with self.subTest("Quality score set"):
            self.assertIsInstance(example_turn.quality, float)
        with self.subTest("Quality score initialised to TfT score"):
            self.assertEqual(example_turn.quality, example_turn.TfT_score)

    def test_representation(self):
        example_turn = Turn(
            index=0, user_utterance="hiya Bob", system_utterance="heya Harry. whats up?"
        )
        self.assertIsInstance(str(example_turn), str)

    def test_link_next_turn(self):
        example_turn_1 = Turn(
            index=0, user_utterance="hiya Bob", system_utterance="heya Harry. whats up?"
        )
        with self.subTest("adding None for next turn"):
            example_turn_1.link_next_turn(next_turn=None)
            self.assertIsNone(example_turn_1.R_score)
            self.assertIsInstance(example_turn_1.quality, float)
            self.assertEqual(example_turn_1.quality, example_turn_1.TfT_score)
        with self.subTest("adding a Turn for next turn"):
            example_turn_2 = Turn(
                index=1,
                user_utterance="nothing much. Just chilling",
                system_utterance="how is work? how is the family?",
            )
            example_turn_1.link_next_turn(next_turn=example_turn_2)
            self.assertIsInstance(example_turn_1.R_score, float)
            self.assertIsInstance(example_turn_1.quality, float)
            self.assertNotEqual(example_turn_1.quality, example_turn_1.TfT_score)


class TestUtterance(TestCase):
    def test_init(self):
        example_utterance = Utterance(
            text="i like cats",
            utterance_index=0,
            minimum_similarity_to_link_entities=0.5,
        )
        with self.subTest("index set"):
            self.assertEqual(example_utterance.index, 0)
        with self.subTest("text set"):
            self.assertEqual(example_utterance.text, "i like cats")
        with self.subTest("_entities_in_text set"):
            self.assertIsInstance(example_utterance._entities_in_text, str)
        with self.subTest("threshold set"):
            self.assertEqual(example_utterance.entity_linking_threshold, 0.5)
        with self.subTest("sentiment set"):
            self.assertIsInstance(example_utterance.sentiment, float)
        with self.subTest("formality set"):
            self.assertIsInstance(example_utterance.formality, float)
        with self.subTest("entities set"):
            self.assertIsInstance(example_utterance.entities, list)

    def test_repr(self):
        example_utterance = Utterance(
            text="i like cats",
            utterance_index=0,
            minimum_similarity_to_link_entities=0.5,
        )
        self.assertIsInstance(str(example_utterance), str)

    def test_mean_semantic_overlap(self):
        example_utterance = Utterance(
            text="i like cats",
            utterance_index=0,
            minimum_similarity_to_link_entities=0.5,
        )
        example_utterance_2 = Utterance(
            text="do you have a kitten",
            utterance_index=1,
            minimum_similarity_to_link_entities=0.5,
        )
        score = example_utterance.mean_semantic_overlap(other=example_utterance_2)
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"{score} >= 0"):
            self.assertGreaterEqual(score, 0.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        with self.subTest("no words in second set produce score of 0."):
            example_utterance_2 = Utterance(
                text="", utterance_index=1, minimum_similarity_to_link_entities=0.5
            )
            score = example_utterance.mean_semantic_overlap(other=example_utterance_2)
            self.assertEqual(score, 0.0)
        with self.subTest("no words in first set produce score of 1."):
            example_utterance_2 = Utterance(
                text="", utterance_index=1, minimum_similarity_to_link_entities=0.5
            )
            score = example_utterance_2.mean_semantic_overlap(other=example_utterance)
            self.assertEqual(score, 1.0)

    def test_highlight_entities(self):
        example_utterance = Utterance(
            text="i like cats",
            utterance_index=0,
            minimum_similarity_to_link_entities=0.5,
        )
        self.assertIsInstance(
            example_utterance._highlight_entities(text="this is a test"), str
        )


class TestEntity(TestCase):
    def test_init(self):
        example_entity = Entity(text="cat", thread_depth=0)
        with self.subTest("text set"):
            self.assertEqual(example_entity.text, "cat")
        with self.subTest("depth set"):
            self.assertEqual(example_entity.depth, 0)
        with self.subTest("semantics set"):
            self.assertIsInstance(example_entity.semantics, ndarray)
        with self.subTest("x coordinate set"):
            self.assertIsInstance(example_entity.x, float)
        with self.subTest("y coordinate set"):
            self.assertIsInstance(example_entity.y, float)
        with self.subTest("children initialised"):
            self.assertIsInstance(example_entity._children, list)
        with self.subTest("parent similarity set to negative value"):
            self.assertLess(example_entity._parent_similarity, 0.0)

    def test_sub(self):
        cat = Entity(text="cat", thread_depth=0)
        kitten = Entity(text="kitten", thread_depth=0)
        score = cat - kitten
        with self.subTest(f"{score} is a real number"):
            self.assertIsInstance(score, float)
        with self.subTest(f"{score} >= 0"):
            self.assertGreaterEqual(score, 0.0)
        with self.subTest(f"{score} <= 1."):
            self.assertLessEqual(score, 1.0)
        car = Entity("car", 0)
        truck = Entity("truck", 1)
        play = Entity("play", 2)
        playing = Entity("playing", 3)
        with self.subTest("car is closer (less distance) to mercedes than play"):
            self.assertLess(car - truck, car - play)
        with self.subTest("play is closer (less distance) to playing than car"):
            self.assertLess(play - playing, playing - car)

    def test_is_thread_head(self):
        example_entity = Entity(text="cat", thread_depth=0)
        self.assertIsInstance(example_entity.is_thread_head(), bool)
        self.assertEqual(example_entity.is_thread_head(), False)

    def test_is_stub(self):
        example_entity = Entity(text="cat", thread_depth=0)
        self.assertIsInstance(example_entity.is_stub(), bool)
        self.assertEqual(example_entity.is_stub(), True)

    def test_is_root(self):
        example_entity = Entity(text="cat", thread_depth=0)
        self.assertIsInstance(example_entity.is_root(), bool)
        self.assertEqual(example_entity.is_root(), True)

    def test_is_linked(self):
        example_entity = Entity(text="cat", thread_depth=0)
        self.assertIsInstance(example_entity.is_linked(), bool)
        self.assertEqual(example_entity.is_linked(), False)

    def test_link(self):
        with self.subTest("link threshold is 1.0"):
            example_entity = Entity(text="fire", thread_depth=0)
            example_entity_2 = Entity(text="fire", thread_depth=1)
            example_entity_3 = Entity(text="flame", thread_depth=1)
            example_entity_4 = Entity(text="cats", thread_depth=1)
            example_entity.link(
                others=[example_entity_2, example_entity_3, example_entity_4],
                similarity_threshold=1.0,
            )
            self.assertIn(example_entity_2, example_entity._children)
            self.assertNotIn(example_entity_3, example_entity._children)
            self.assertNotIn(example_entity_4, example_entity._children)
        with self.subTest("link threshold is 0.0"):
            example_entity = Entity(text="fire", thread_depth=0)
            example_entity_2 = Entity(text="fire", thread_depth=1)
            example_entity_3 = Entity(text="flame", thread_depth=1)
            example_entity_4 = Entity(text="cats", thread_depth=1)
            example_entity.link(
                others=[example_entity_2, example_entity_3, example_entity_4],
                similarity_threshold=0.0,
            )
        with self.subTest("link threshold is .7"):
            example_entity = Entity(text="fire", thread_depth=0)
            example_entity_2 = Entity(text="fire", thread_depth=1)
            example_entity_3 = Entity(text="flame", thread_depth=1)
            example_entity_4 = Entity(text="cats", thread_depth=1)
            example_entity.link(
                others=[example_entity_2, example_entity_3, example_entity_4],
                similarity_threshold=0.7,
            )
            self.assertIn(example_entity_2, example_entity._children)
            self.assertIn(example_entity_3, example_entity._children)
            self.assertNotIn(example_entity_4, example_entity._children)

    def test_y_coordinate(self):
        example_entity = Entity(text="cat", thread_depth=0)
        self.assertIsInstance(example_entity._y_coordinate(), float)

    def test_x_coordinate(self):
        example_entity = Entity(text="cat", thread_depth=0)
        self.assertIsInstance(example_entity._x_coordinate(), float)
        with self.subTest("coordinate is projected the same way each time"):
            x_1 = example_entity._x_coordinate()
            x_2 = example_entity._x_coordinate()
            self.assertEqual(x_1, x_2)


if __name__ == "__main__":
    main()
