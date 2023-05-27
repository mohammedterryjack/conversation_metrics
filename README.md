# Automatic Evaluation of Conversation Quality

## Installation
```
pip install git+https://conversation_metrics:ykzJYb-StfQHHpriwe6z@git.oxolo.com/development/oxolo-kids-nlp/packages/conversation-metrics.git
```

---

## Analysis Example
```python
from conversation_metrics import Conversation

example = '''i am bored!
do you want to play a game?
yeah - but what game?
i know many games. how about rock, paper, scissors'''
my_conversation = Conversation(example)

```

```python
print(my_conversation)
```
![](images/example_conversation.png)

```python
my_conversation.display_scores()
```
![](images/example_scores_plot.png)

```python
my_conversation.display_threads()
```
![](images/example_entity_threads_weighted_plot.png)

---

## Alternatively
`interact.py` will let you analyse a conversation as you create it (in real-time)

---
## Rank and Select Example 

```python
from conversation_metrics import select_highest_quality_reply

select_highest_quality_reply(
    utterance="this is a lovely test",
    replies=[
        "how do you know",
        "what's so lovely about this test",
        "what do you mean?",
    ],
)
```
```
>>  "what's so lovely about this test"
```

If you want to see the scores of each candidate reply:

```python
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
```
```
>>> [-.435, 1.0, -.435]
```
and if you want to speed things up you can pass you own custom models (do this before loading in conversation_metrics.Conversaion if you want to avoid default models being loaded in)

e.g.
```python
Conversation(
    conversation=example,
    measure_formality=lambda text:1.0,
    measure_sentiment=lambda text:-1.0,
    extract_entities=lambda text:['entity1','entity2'],
    vectorise=lambda entity:[0.2,-0.9,...,0.5],
)
```

---
## Metrics

The theory behind these conversation metrics are explained [here](https://docs.google.com/document/d/1U9l93l_vhNrocfd2Hj_yaqGap7n-dMDDgaNouZluglI/edit#heading=h.cfltg1r7qrwd)


In summary: a conversation is automatically analysed on a turn-by-turn basis using these novel metrics to produce a turn `Quality` (informed via more fundamental metrics like the `Tit-for-tat` and `Inferred Reaction`, which are themselves based upon certain signals extracted from the conversation).

![](images/example_entity_threads.png)
![](images/example_entity_threads_plot.png)

The threads discussed throughout the conversational are also extracted and can also be viewed as connected/linked chains of like-entities (Note: how a single conversation often contains multiple conversation threads and it is common for more than one thread can be held in parallel)

---
## Structures
This is where the conversation is put into a hierarchical structures as follows:
- `Conversation`
    - `Turn`
        - `Utterance`
            - `Entity`

The file `settings.py` is a centralised place to store all the default values used for formatting plots and other displays

---
## Annotators
The various models used to extract raw signals and data from the conversation. This information is later used by the automatic conversation metrics to analyse the conversation.  

E.g. 
- `Sentiment` (to measure the positivity/negativity/neutrality of a given utterance)
- `Formality` (to measure how formal (personal) or informal (impersonal) an utterance is)
- `EntityExtractor` ( to extract the words in the utterance which carry the most meaning (i.e. the nouns and verbs))

Some of the models simply convert the string to another form:

E.g.
- `SemanticEncoder` (to encode the semantics of text)
- `StringPreprocessor` (a lightweight preprocessor for simple string manipulation)

---
## Future Updates

- update `Conversation` to load in text files
- update the `Formality` annotator from a lookup heuristic to a custom trained model
- update the `Sentiment` annotator from huggingface to model hosted on Triton

---
## ChangeLogs
- 1.0.3:
  - Allows custom models to be passed for faster load and inference times
- 1.0.2:
  - Added methods to rank replies and select the one with highest quality 
- 1.0.1:
  - Normalising Tit-for-Tat score to be between -1 to 1
  - Allowing for plots to be saved to file
- 1.0.0: 
  - First release of package