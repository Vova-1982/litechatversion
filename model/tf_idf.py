import nltk
from model.replika_set import data_set
import random
from model.text_preprocessing import clear_special_characters
from model.models import TfIdfConfig


def classify_intent(replica):
    rez_intent = None
    replica = clear_special_characters(replica)
    intent = TfIdfConfig.clf.predict(TfIdfConfig.vectorizer.transform([replica]))[0]

    examples = data_set['intents'][intent]['examples']

    for example in examples:
        example = clear_special_characters(example)
        if len(example) > 0:
            distance = nltk.edit_distance(replica, example)
            if distance / len(example) < TfIdfConfig.min_koef_distance__tf_idf:
                rez_intent = intent
    return rez_intent

def answer_generation(intent, lang):
    responses = data_set['intents'][intent][f'responses_{lang}']
    return random.choice(responses)


if __name__ == "__main__":

    question = '''Как дела'''
    intent = classify_intent(question)
    print(intent)
    input('===')
    print(answer_generation(intent, lang = "ru"))
