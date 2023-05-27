from conversation_metrics import Conversation

example_conversation = Conversation(
    """this is a test
    what kind of test?
    just a small chat about nothing!
    ooh you mean about space?
    no! space is not nothing. It is something!
    so what is nothing?
    how can i explain it to you
    just try explaining it to me
    i'm talking about an abstract concept 
    its best to give concrete examples or analogies then""",
)
print(example_conversation)
example_conversation.display_scores()
example_conversation.display_threads()


from conversation_metrics import evaluate_replies

qualities = evaluate_replies(
    utterance="this is a lovely test",
    replies=[
        "how do you know",
        "what's so lovely about this test",
        "what do you mean?",
    ],
)
print(list(qualities))


from conversation_metrics import select_highest_quality_reply

print(
    select_highest_quality_reply(
        utterance="this is a lovely test",
        replies=[
            "how do you know",
            "what's so lovely about this test",
            "what do you mean?",
        ],
    )
)

print(
    select_highest_quality_reply(
        utterance="this is a lovely test",
        replies=[
            "how do you know",
            "what's so lovely about this test",
            "what do you mean?",
        ],
        measure_formality=lambda text: 1.0,
        measure_sentiment=lambda text: -1.0,
        extract_entities=lambda text: ["entity1", "entity2"],
        vectorise=lambda entity: [0.2, -0.9, 0.5],
    )
)
