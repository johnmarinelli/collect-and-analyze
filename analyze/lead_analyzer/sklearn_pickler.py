from sklearn.externals import joblib

from django.conf import settings

import os

PICKLE_JAR = os.path.join(settings.ROOT_DIR, 'analyze', 'sklearn_models')
COUNT_VECTORIZER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'countvectorizer.pkl')
TFIDF_TRANSFORMER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'tfidftransfomer.pkl')
CLASSIFIER_PICKLE_PATH = os.path.join(PICKLE_JAR, 'clf.pkl')

class PickleLoader:
    def pickles_exist(self):
        return (os.path.exists(PICKLE_JAR) and
          os.path.exists(COUNT_VECTORIZER_PICKLE_PATH) and
          os.path.exists(TFIDF_TRANSFORMER_PICKLE_PATH) and
          os.path.exists(CLASSIFIER_PICKLE_PATH))

    def load_pickle(self, path):
        return joblib.load(path)

class PickleSaver:
    def save_pickle(obj, path):
        return joblib.dump(obj, path)
