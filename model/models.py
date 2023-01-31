from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from model.replika_set import data_set
from model.text_preprocessing import clear_special_characters


class TfIdfConfig:
    try:
        set_answer = data_set
        texts = []
        intent_names = []
        stats = {'intents': 0, 'generative': 0, 'stubs': 0}

        for intent, intent_data in set_answer['intents'].items():
            for example in intent_data['examples']:
                texts.append(clear_special_characters(example))
                intent_names.append(intent)

        vectorizer = TfidfVectorizer(ngram_range=(2, 4), analyzer='char')
        X = vectorizer.fit_transform(texts)
        clf = LinearSVC()
        clf.fit(X, intent_names)

        min_koef_distance__tf_idf = 0.2

    except Exception as ex:
        raise ex