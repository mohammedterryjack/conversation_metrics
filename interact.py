from conversation_metrics import Conversation

example_conversation = Conversation()
while True:
    example_conversation.add_utterance(input("User: "))
    example_conversation.add_utterance(input("System: "))
    print(example_conversation)
    example_conversation.display_scores()
    example_conversation.display_threads()
