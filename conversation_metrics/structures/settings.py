from enum import Enum


class ConversationSettings(Enum):
    THREAD_BORDER = "+++++++++++++++"
    TURN_BORNER = "-------------"
    THREAD_HEADER = "\nTHREAD:\n"
    TURN_CONNECTOR = "\n"
    UTTERANCE_DELIMITER = "\n"
    SCORE_PLACEHOLDER = "..."
    INDENTATION = "  "

    SCORES_TITLE = "Scores"
    TURN_LABEL = "Turn #"
    SCORES_X_LABEL = "Utterance #"
    QUALITY_LABEL = "Quality"
    TIT_FOR_TAT_LABEL = "Tit-for-Tat"
    INFERRED_REACTION_LABEL = "Reaction"
    SENTIMENT_LABEL = "Sentiment"
    FORMALITY_LABEL = "Formality"
    THREADS_Y_LABEL = "Conversation Depth"
    THREADS_X_LABEL = "Relative Meaning"
    USER_LABEL = "USER"
    SYSTEM_LABEL = "SYSTEM"

    SENTIMENT_COLOUR = "pink"
    FORMALITY_COLOUR = "purple"
    USER_TEXT_COLOUR = "red"
    SYSTEM_TEXT_COLOUR = "blue"
    LINK_COLOUR = "grey"

    USER_BOUNDING_BOX = dict(boxstyle="round", fc="pink", ec="violet")
    SYSTEM_BOUNDING_BOX = dict(boxstyle="round", fc="orange", ec="blue")

    CONVERSATION_REPRESENTATION = """{turn_repreesentation}
{border}
{thread_representation}
{border}"""
    TURN_REPRESENTATION = """
        {turn_label}{turn_number}:    

            {user_label}: {user_utterance}
            {system_label}: {system_utterance}
            {border}
            {quality_label} = {quality_score}
                ({tft_label} = {tft_score})
                ({r_label} = {r_score})
            {border}
    """
    UTTERANCE_REPRESENTATION = """{utterance}
                ({sentiment_label} = {sentiment_score})
                ({formality_label} = {formality_score})
    """
    ENTITY_REPRESENTATION = """{indentation}{entity_text} ({link_weight})"""

    TURN_UTTERANCE_ALIGNMENT_FACTOR = 2
    TURN_START_OFFSET = 1
    SCORES_NUMBER_OF_GRAPHS = 2
    THREADS_MINIMUM_X = -1
    THREADS_MAXIMUM_X = 1
    THREADS_MAXIMUM_Y = 1
    ROUND_TO = 2
    RANDOM_PROJECTION_SEED = 1
    LINK_WIDTH = 2

    SCORES_LINE_STRENGTH = 0.7
    LEGEND_USER_LABEL_Y_COORDINATE = 0.55
    LEGEND_USER_LABEL_X_COORDINATE = 0.0
    LEGEND_SYSTEM_LABEL_Y_COORDINATE = 0.75
    LEGEND_SYSTEM_LABEL_X_COORDINATE = 0.0
    LINK_SIMILARITY_THRESHOLD = 0.65
    MAX_OVERLAP_SCORE = 1.0
    MIN_OVERLAP_SCORE = 0.0
    SENTIMENT_NORMALISATION_FACTOR = 0.5
    MAX_PROJECTION_WEIGHT = 10.0
    MIN_PROJECTION_WEIGHT = -10.0
    IMPOSSIBLE_ENTITY_SIMILARITY = -1.0
